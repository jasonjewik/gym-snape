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
+----------------------------------------------------------------+
| TURN: 82 | LIVES: 1  | TROPHIES: 10 | GOLD: 0  | ACTIONS: 3366 |
+----------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|HIPPO     ||          ||          ||          ||          |
|hp:  27   ||          ||          ||          ||          |
|atk: 23   ||          ||          ||          ||          |
|fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||          ||          ||          ||          |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|RHINO    *||COW       ||SCORPION  ||RHINO    *||TURKEY    ||PIZZA     ||MUSHROOM  |
|hp:  44   ||hp:  24   ||hp:  19   ||hp:  50   ||hp:  22   ||          ||          |
|atk: 41   ||atk: 22   ||atk: 19   ||atk: 50   ||atk: 21   ||          ||          |
|fct: ...  ||fct: ...  ||fct: Psn  ||fct: ...  ||fct: ...  ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
You won!
PLAYER 2
+----------------------------------------------------------------+
| TURN: 82 | LIVES: 0  | TROPHIES: 9  | GOLD: 0  | ACTIONS: 3372 |
+----------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||          ||          ||          |
|          ||          ||          ||          ||          |
|          ||          ||          ||          ||          |
|          ||          ||          ||          ||          |
|          ||          ||          ||          ||          |
|          ||          ||          ||          ||          |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|CROCODILE*||SCORPION  ||ROOSTER  *||LEOPARD   ||TIGER    *||PEAR      ||MELON     |
|hp:  50   ||hp:  33   ||hp:  50   ||hp:  36   ||hp:  35   ||          ||          |
|atk: 50   ||atk: 33   ||atk: 50   ||atk: 42   ||atk: 36   ||          ||          |
|fct: ...  ||fct: Psn  ||fct: ...  ||fct: ...  ||fct: ...  ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
You lost!
```
