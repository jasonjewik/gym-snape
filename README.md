# Super Nifty Auto Pets Environment (SNAPE)

I'm tired of losing consistently in _[Super Auto Pets](https://store.steampowered.com/app/1714040/Super_Auto_Pets/)_, so I made this environment to train an RL agent to play for me.

This repository comes with a playable version of _Super Auto Pets_. See `gym-snape/gym_snape/game/README.md` for details.

Currently tested only on Windows.

## Installation

```shell
$ conda env create -f conda_envs/windows.yml
$ conda activate snape
$ pip install -e gym-snape
```

## Example

Pit two agents that pick actions randomly against each other.

```python
>>> python example.py
```

Sample output:

```text
This game has ended. No further actions can be taken.
This game has ended. No further actions can be taken.
PLAYER 1
+---------------------------------------------------------------+
| TURN: 15 | LIVES: 0  | TROPHIES: 2  | GOLD: 7  | ACTIONS: 536 |
+---------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||MOSQUITO  ||PIG       ||SLOTH     |
|          ||          ||hp:  3    ||hp:  1    ||hp:  2    |
|          ||          ||atk: 3    ||atk: 3    ||atk: 2    |
|          ||          ||fct: ...  ||fct: ...  ||fct: ...  |
|          ||          ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  |
|          ||          ||lvl: 1    ||lvl: 1    ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|FISH      ||SLOTH     ||HORSE     ||BEAVER    ||          ||APPLE*    ||APPLE*    |
|hp:  3    ||hp:  1    ||hp:  1    ||hp:  2    ||          ||          ||          |
|atk: 2    ||atk: 1    ||atk: 2    ||atk: 2    ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
You lost!
PLAYER 2
+---------------------------------------------------------------+
| TURN: 15 | LIVES: 8  | TROPHIES: 10 | GOLD: 10 | ACTIONS: 537 |
+---------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||ANT       ||HORSE     ||MOSQUITO  ||FISH      |
|          ||hp:  1    ||hp:  2    ||hp:  2    ||hp:  4    |
|          ||atk: 2    ||atk: 2    ||atk: 2    ||atk: 2    |
|          ||fct: ...  ||fct: ...  ||fct: ...  ||fct: ...  |
|          ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  |
|          ||lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|MOSQUITO  ||PIG       ||FISH      ||OTTER     ||CRICKET   ||HONEY     ||HONEY     |
|hp:  2    ||hp:  1    ||hp:  3    ||hp:  2    ||hp:  2    ||          ||          |
|atk: 2    ||atk: 3    ||atk: 2    ||atk: 1    ||atk: 1    ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||fct: ...  ||fct: ...  ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
You won!
```
