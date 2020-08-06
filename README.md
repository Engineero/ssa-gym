# ssa-gym
This is a repository of an OpenAI Gym environment for tasking Space Situational Awareness Sensors and some associated agents.

Original repository author : Maj. Ashton Harvey, Devayani Pawar

The repository includes:
* [Data Source and Transformation functions](envs/transformations.py)
* [Source code of SSA tasker](envs/ssa_tasker_simple_2.py)
* [filter.py](envs/filter.py) is an extract of Roger Labbe's FilterPy (https://filterpy.readthedocs.io/) 
* [Test Cases](tests.py)
* [Results and Plots](envs/results.py)

## Requirements
Python 3.6, and other common packages listed in `requirements.txt`.

## Installation
1. Clone this repository
2. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
3. [optional] Run setup from the repository root directory
    ```bash
    python3 setup.py install
    ``` 
## Getting Started:


[Register's environment with Gym](envs/__init__.py )


#### Key Concepts used:
- Deep Reinforcement Learning : https://spinningup.openai.com/en/latest/

#### Libraries used
- Reinforcement Learning in python: https://gym.openai.com/docs/
- Astropy - A Community Python Library for Astronomy: https://www.astropy.org/
- FilterPy - Python library that implements a number of Bayesian filters, most notably Kalman filters: https://filterpy.readthedocs.io/en/latest/
- Numba - Numba is an open source JIT compiler that translates a subset
 of Python and NumPy code into fast machine code: http://numba.pydata.org/

## Viz

## References:

## Citation
```
@misc{ssa-gym_2020,
  title={An OpenAI Gym environment for tasking Space Situational Awareness Sensors and some associated agents.
},
  author={Maj. Ashton Harvey, Devayani Pawar},
  year={2020},
  publisher={Github},
  journal={GitHub repository},
  howpublished={\url{https://github.com/AshHarvey/ssa-gym}},
}
```



