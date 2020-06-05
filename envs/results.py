import numpy as np
from scipy.spatial import distance
from numba import njit


@njit
def errors(states, filters_x, filters_diag_P):
    n, m, d = states.shape # Timesteps dimension, RSO dimension, dimension of x
    sigma_position = np.zeros(shape=(n, m)) # magnitude of position uncertainty (meters)
    sigma_velocity = np.zeros(shape=(n, m)) # magnitude of velocity uncertainty (meters)
    delta_position = np.zeros(shape=(n, m)) # mean position - true position (meters)
    delta_velocity = np.zeros(shape=(n, m)) # mean velocity - true velocity (meters)
    for i in range(n): # Timesteps dimension
        delta_position[i, :] = dist3d(filters_x[i][:, :3], states[0][:, :3])
        delta_velocity[i, :] = dist3d(filters_x[i][:, 3:], states[0][:, 3:])
        sigma_position[i, :] = var3d(filters_diag_P[i][:, :3])
        sigma_velocity[i, :] = var3d(filters_diag_P[i][:, 3:])
    return delta_position, delta_velocity, sigma_position, sigma_velocity


@njit
def error(states, obs):
    delta_position = dist3d(obs[:, :3], states[:, :3]) # mean position - true position (meters)
    delta_velocity = dist3d(obs[:, 3:6], states[:, 3:]) # mean velocity - true velocity (meters)
    sigma_position = var3d(obs[:, 6:9]) # magnitude of position uncertainty (meters)
    sigma_velocity = var3d(obs[:, 9:]) # magnitude of velocity uncertainty (meters)
    return delta_position, delta_velocity, sigma_position, sigma_velocity


@njit
def error_failed(state, x, P):
    result = np.zeros(4)
    result[0] = np.sqrt(np.sum((x[:3]-state[:3])**2)) # mean position - true position (meters)
    result[1] = np.sqrt(np.sum((x[3:]-state[3:])**2)) # mean velocity - true velocity (meters)
    result[2] = np.sqrt(np.sum(np.diag(P)[:3])) # magnitude of position uncertainty (meters)
    result[3] = np.sqrt(np.sum(np.diag(P)[3:])) # magnitude of velocity uncertainty (meters)
    return result


@njit
def observations(filters_x, filters_P):
    n = len(filters_x)
    observation = np.zeros((n, 12))
    for i in range(n):
        observation[i,:6] = filters_x[i]
        observation[i,6:] = np.diag(filters_P[i])
    return observation


@njit
def dist3d(u, v):
    dist = np.sqrt(np.sum((u-v)**2, axis=1))
    return dist

@njit
def var3d(u):
    dist = np.sqrt(np.sum(u, axis=1))
    return dist


def obs_filter_object_x_diagP(filters):
    obs = []
    for ukf in filters:
        obs.append(np.append(ukf.x,np.diag(ukf.P)))

    obs = np.array(obs)

    return np.nan_to_num(obs,nan=99999, posinf=99999)


def plot_results(states, filters_x, filters_P, t, title=None):
    # obtain number for initial error plots
    errors_position, errors_velocity, filter_error_position, filter_error_velocity = errors(states, filters_x, filters_P)
    #create a figure
    #plt.subplots_adjust(top=0.9)
    fig = plt.figure(figsize=(24,12),dpi=200)
    if not(title==None):
        fig.suptitle(title)
    ax = fig.add_subplot(121)
    #plot to first axes
    palette = sns.color_palette("hls",len(filter_error_position))
    for j in range(len(filter_error_position)):
        ax.plot(t,filter_error_position[j],color=palette[j],label="Magnitude of Filter's Position $\sigma$")
        ax.plot(t,filter_error_velocity[j],color=palette[j],label="Magnitude of Filter's Velocity $\sigma$")

    ax.set_ylabel('Error in meters (log scale)')
    ax.set_yscale('log')
    #create twin axes
    '''
    ax2=ax.twinx()
    #plot to twin axes
    for j in range(len(obs_steps)):
        ax2.scatter(obs_steps[j], np.degrees(Elevation[j]), s=80, alpha=0.7, color=palette[j], zorder=3, marker='.', label='Observations'); 
    ax2.set_ylabel('Elevation in Degrees')
    
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    handles = [copy.copy(h1[1])]
    handles.append(copy.copy(h1[1]))
    for handle in handles:
        color = (0,0,0)
        handle._color = color
    handles.append(copy.copy(h2[0]))
    handles[-1]._edgecolors = np.asarray([[0,0,0,0.3]])
    handles[-1]._facecolors = np.asarray([[0,0,0,0.3]])
    labels = l1[:2]
    labels += [l2[0]]
    ax.legend(handles=handles, labels=labels, loc='upper left')
    '''

    ax = fig.add_subplot(122)
    #plot to first axes
    for j in range(len(errors_position)):
        ax.plot(t,errors_position[j],color=palette[j],label="Magnitude of Position Error")
        ax.plot(t,errors_velocity[j],color=palette[j],label="Magnitude of Velocity Error")
    ax.set_ylabel('Error in meters (log scale)')
    ax.set_yscale('log')
    #create twin axes
    '''
    ax2=ax.twinx()
    #plot to twin axes
    for j in range(len(obs_steps)):
        ax2.scatter(obs_steps[j], np.degrees(Elevation[j]), s=80, alpha=0.3, color=palette[j], zorder=3, marker='.', label='Observations'); 
    ax2.set_ylabel('Elevation in Degrees')
    
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    handles = [copy.copy(h1[1])]
    handles.append(copy.copy(h1[1]))
    for handle in handles:
        color = (0,0,0)
        handle._color = color
    handles.append(copy.copy(h2[0]))
    handles[-1]._edgecolors = np.asarray([[0,0,0,0.3]])
    handles[-1]._facecolors = np.asarray([[0,0,0,0.3]])
    labels = l1[:2]
    labels += [l2[0]]
    ax.legend(handles=handles, labels=labels, loc='upper left')
    '''
    plt.show()