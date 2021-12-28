# Playing _Super Auto Pets: Unofficial Terminal Edition_

## Usage

### Creating a 2-player game

```python
>>> from gym_snape.game import Game
>>> player1 = Game()
>>> player2 = Game()
```

If a game instance is initialized with `display=True`, the state of the game will be displayed after most commands (see example below).

### Displaying the game

```python
>>> player1()
```

This can also be done with an explicit print call, like `print(player1)`.

### Rolling the shop

```python
>>> player1.roll()
```

### Freezing a shop slot

```python
>>> player1.freeze(shop_index)
```

### Purchasing a shop item

```python
>>> player1.buy(shop_index, deck_index)
```

This can also be achieved by passing in a 2-tuple like `player1.buy((shop_index, deck_index))`.

### Selling a deck pet

```python
>>> player1.sell(deck_index)
```

### Swapping two deck slots

```python
>>> player1.swap(source_index, destination_index)
```

This can also be achieved by passing in a 2-tuple like `player1.swap((source_index, destination_index))`.

### Merging two deck slots

```python
>>> player1.merge(source_index, destination_index)
```

This can also be achieved by passing in a 2-tuple like `player1.merge((source_index, destination_index))`.

### Combat

```python
>>> player1.challenge(player2)
```

## Example

```python
>>> from gym_snape.game import Game
>>> p1 = Game(display=True)  # create player 1
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 | ACTIONS: 1  |
+--------------------------------------------------------------+
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
|PIG       ||HORSE     ||ANT       ||          ||          ||HONEY     ||          |
|hp:  1    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
|atk: 3    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p2 = Game(display=True)  # create player 2
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 | ACTIONS: 1  |
+--------------------------------------------------------------+
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
|MOSQUITO  ||MOSQUITO  ||ANT       ||          ||          ||HONEY     ||          |
|hp:  2    ||hp:  2    ||hp:  1    ||          ||          ||          ||          |
|atk: 2    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p1.buy(1,2)  # buy shop slot 1, place into deck slot 2
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 7  | ACTIONS: 2  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||HORSE     ||          ||          |
|          ||          ||hp:  1    ||          ||          |
|          ||          ||atk: 2    ||          ||          |
|          ||          ||fct: ...  ||          ||          |
|          ||          ||exp: 0/2  ||          ||          |
|          ||          ||lvl: 1    ||          ||          |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|PIG       ||          ||ANT       ||          ||          ||HONEY     ||          |
|hp:  1    ||          ||hp:  1    ||          ||          ||          ||          |
|atk: 3    ||          ||atk: 2    ||          ||          ||          ||          |
|fct: ...  ||          ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||          ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||          ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p1.buy(2,0)  # buy shop slot 2, place into deck slot 0
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 4  | ACTIONS: 3  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||HORSE     ||          ||ANT       |
|          ||          ||hp:  1    ||          ||hp:  1    |
|          ||          ||atk: 2    ||          ||atk: (3)  |
|          ||          ||fct: ...  ||          ||fct: ...  |
|          ||          ||exp: 0/2  ||          ||exp: 0/2  |
|          ||          ||lvl: 1    ||          ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|PIG       ||          ||          ||          ||          ||HONEY     ||          |
|hp:  1    ||          ||          ||          ||          ||          ||          |
|atk: 3    ||          ||          ||          ||          ||          ||          |
|fct: ...  ||          ||          ||          ||          ||          ||          |
|exp: 0/2  ||          ||          ||          ||          ||          ||          |
|lvl: 1    ||          ||          ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p1.roll()  # roll the shop
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 3  | ACTIONS: 4  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||HORSE     ||          ||ANT       |
|          ||          ||hp:  1    ||          ||hp:  1    |
|          ||          ||atk: 2    ||          ||atk: (3)  |
|          ||          ||fct: ...  ||          ||fct: ...  |
|          ||          ||exp: 0/2  ||          ||exp: 0/2  |
|          ||          ||lvl: 1    ||          ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|MOSQUITO  ||CRICKET   ||OTTER     ||          ||          ||APPLE     ||          |
|hp:  2    ||hp:  2    ||hp:  2    ||          ||          ||          ||          |
|atk: 2    ||atk: 1    ||atk: 1    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p1.buy(2,1)  # buy from shop slot 2, place into deck slot 1
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 0  | ACTIONS: 5  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||HORSE     ||OTTER     ||ANT       |
|          ||          ||hp:  1    ||hp:  2    ||hp:  2    |
|          ||          ||atk: 2    ||atk: (2)  ||atk: (4)  |
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
|MOSQUITO  ||CRICKET   ||          ||          ||          ||APPLE     ||          |
|hp:  2    ||hp:  2    ||          ||          ||          ||          ||          |
|atk: 2    ||atk: 1    ||          ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||          ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||          ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p2()  # display player 2's game
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 | ACTIONS: 1  |
+--------------------------------------------------------------+
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
|MOSQUITO  ||MOSQUITO  ||ANT       ||          ||          ||HONEY     ||          |
|hp:  2    ||hp:  2    ||hp:  1    ||          ||          ||          ||          |
|atk: 2    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p2.buy(0,1)  # buy shop slot 0, place into deck slot 1
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 7  | ACTIONS: 2  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||          ||MOSQUITO  ||          |
|          ||          ||          ||hp:  2    ||          |
|          ||          ||          ||atk: 2    ||          |
|          ||          ||          ||fct: ...  ||          |
|          ||          ||          ||exp: 0/2  ||          |
|          ||          ||          ||lvl: 1    ||          |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|          ||MOSQUITO  ||ANT       ||          ||          ||HONEY     ||          |
|          ||hp:  2    ||hp:  1    ||          ||          ||          ||          |
|          ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
|          ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|          ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|          ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p2.buy(1,1)  # buy shop slot 1, place into deck slot 1
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 4  | ACTIONS: 3  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||          ||MOSQUITO  ||          |
|          ||          ||          ||hp:  3    ||          |
|          ||          ||          ||atk: 3    ||          |
|          ||          ||          ||fct: ...  ||          |
|          ||          ||          ||exp: 1/2  ||          |
|          ||          ||          ||lvl: 1    ||          |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|          ||          ||ANT       ||          ||          ||HONEY     ||          |
|          ||          ||hp:  1    ||          ||          ||          ||          |
|          ||          ||atk: 2    ||          ||          ||          ||          |
|          ||          ||fct: ...  ||          ||          ||          ||          |
|          ||          ||exp: 0/2  ||          ||          ||          ||          |
|          ||          ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p2.buy(2,0)  # buy shop slot 2, place into deck slot 0
```

```text
+--------------------------------------------------------------+
| TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 1  | ACTIONS: 4  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||          ||MOSQUITO  ||ANT       |
|          ||          ||          ||hp:  3    ||hp:  1    |
|          ||          ||          ||atk: 3    ||atk: 2    |
|          ||          ||          ||fct: ...  ||fct: ...  |
|          ||          ||          ||exp: 1/2  ||exp: 0/2  |
|          ||          ||          ||lvl: 1    ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|          ||          ||          ||          ||          ||HONEY     ||          |
|          ||          ||          ||          ||          ||          ||          |
|          ||          ||          ||          ||          ||          ||          |
|          ||          ||          ||          ||          ||          ||          |
|          ||          ||          ||          ||          ||          ||          |
|          ||          ||          ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```

```python
>>> p1.challenge(p2)  # the two players enter a battle
```

```text
__   __
\ \ / /__ _  _
 \ V / _ \ || |
  |_|\___/\_,_|
+--------------------------------------------------------------+
| TURN: 2  | LIVES: 10 | TROPHIES: 1  | GOLD: 10 | ACTIONS: 6  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||HORSE     ||OTTER     ||ANT       |
|          ||          ||hp:  1    ||hp:  2    ||hp:  2    |
|          ||          ||atk: 2    ||atk: 1    ||atk: 3    |
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
|BEAVER    ||SLOTH     ||CRICKET   ||          ||          ||HONEY     ||          |
|hp:  2    ||hp:  1    ||hp:  2    ||          ||          ||          ||          |
|atk: 2    ||atk: 1    ||atk: 1    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
 ___
| __|__  ___
| _/ _ \/ -_)
|_|\___/\___|
+--------------------------------------------------------------+
| TURN: 2  | LIVES: 9  | TROPHIES: 0  | GOLD: 10 | ACTIONS: 5  |
+--------------------------------------------------------------+
 ___         _
|   \ ___ __| |__
| |) / -_) _| / /
|___/\___\__|_\_\
4----------43----------32----------21----------10----------0
|          ||          ||          ||MOSQUITO  ||ANT       |
|          ||          ||          ||hp:  3    ||hp:  1    |
|          ||          ||          ||atk: 3    ||atk: 2    |
|          ||          ||          ||fct: ...  ||fct: ...  |
|          ||          ||          ||exp: 1/2  ||exp: 0/2  |
|          ||          ||          ||lvl: 1    ||lvl: 1    |
4----------43----------32----------21----------10----------0
 ___ _
/ __| |_  ___ _ __
\__ \ ' \/ _ \ '_ \
|___/_||_\___/ .__/
             |_|
0----------01----------12----------23----------34----------45----------56----------6
|CRICKET   ||PIG       ||OTTER     ||          ||          ||APPLE     ||          |
|hp:  2    ||hp:  1    ||hp:  2    ||          ||          ||          ||          |
|atk: 1    ||atk: 3    ||atk: 1    ||          ||          ||          ||          |
|fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
|exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
|lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
0----------01----------12----------23----------34----------45----------56----------6
Game ongoing...
```