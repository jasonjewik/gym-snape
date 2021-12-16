# Super Nifty Auto Pets Environment (SNAPE)

I'm tired of losing consistently in [Super Auto Pets](https://store.steampowered.com/app/1714040/Super_Auto_Pets/), so I made this environment to train an RL agent to play for me.

Currently tested only on Windows.

## Installation

```
$ conda env create -f conda_envs/windows.yml
$ conda activate snape
$ pip install -e gym-snape
```

## Testing the environment

To test the environment, use the following command. If no game configuration is passed via `--config`, the script will check the environment using the default configuration at `configs/default`.

```
$ python check_env.py [--config CONFIG_DIRECTORY]
```

If changes are made to the environment at `gym-snape/gym_snape/envs/game_env.py`, one can hot-reload and test with the `-m` flag:

```
$ python check_env.py -m gym-snape
```
