# Super Nifty Auto Pets Environment (SNAPE)

I'm tired of losing consistently in [Super Auto Pets](https://store.steampowered.com/app/1714040/Super_Auto_Pets/), so I made this environment to train an RL agent to play for me.

Currently tested only on Windows.

Installation:

```
$ conda env create -f conda_envs/windows.yml
$ pip install -e gym-snape
$ python
>>> import gym
>>> env = gym.make('gym_snape:snape-v0', config_file='default_config.json')
```
