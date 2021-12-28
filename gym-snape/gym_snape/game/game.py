# Standard library imports
from copy import deepcopy
from functools import wraps
from collections.abc import Callable
from typing import Any, Final, Optional, ParamSpec, Tuple, TypeVar

# Local application imports
from gym_snape.game.deck import Deck
from gym_snape.game.pets import Pet
from gym_snape.game.shop import Shop, ShopItem

# Typing definitions
P = ParamSpec('P')
T = TypeVar('T')
SrcDstPair = Tuple[int, int]


def display_game(class_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Game`'s methods that prints the state of the game after
    the decorated method is called."""
    @wraps(class_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        result = class_method(self, *args, **kwargs)
        if self.display:
            print(self)
        return result
    return _impl


def check_game_over(class_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Game`'s methods that turns each method into a no-op
    once a game over (win or loss) is detected."""
    @wraps(class_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        if not self.game_over:
            result = class_method(self, *args, **kwargs)
            return result
        else:
            print('This game has ended. No further actions can be taken.')
    return _impl


class Game:
    """
    The game.

    Parameters
    ----------
    display: bool
        If True, print the state of the game after each execution of a
        public method (except for `challenge`, see that method for details). 
        If False (default), public methods are executed without displaying 
        the resulting state of the game.
    """

    def __init__(self, display: bool = False):
        self.deck = Deck()
        self.shop = Shop()

        self._turn = 1
        self._n_lives = 10
        self._n_trophies = 0
        self._TROPHIES_TO_WIN: Final = 10
        self._n_gold = 10
        self._GOLD_PER_TURN: Final = 10

        self._ROLL_COST: Final = 1

        self.display = display
        self._n_actions_taken = 0
        self.roll(is_turn_start=True)

    def __str__(self):
        """
        Returns the state of the game in three parts.

        The first part is a status bar which shows the current turn, the
        number of remaining lives, the number of trophies won, the number of
        remaining gold coins, and the number of actions taken. The second part 
        is the current deck, and the third part is the current shop.

        ASCII art courtesy of https://patorjk.com/software/taag/.

        See also
        ----------
        - `gym_snape.game.pets.pet`
        - `gym_snape.game.food.food`
        """

        # The status bar
        width = 2
        status = ' | '.join([
            f'TURN: {self._turn:<{width}}',
            f'LIVES: {self._n_lives:<{width}}',
            f'TROPHIES: {self._n_trophies:<{width}}',
            f'GOLD: {self._n_gold:<{width}}',
            f'ACTIONS: {self.actions_taken:<{width}}'
        ])
        status = '| ' + status + ' |\n'
        border = '+' + '-' * (len(status) - 3) + '+\n'
        status = border + status + border.strip()

        # The deck
        deck_str = [
            ' ___         _   ',
            '|   \\ ___ __| |__',
            '| |) / -_) _| / /',
            '|___/\\___\\__|_\\_\\',
        ]
        deck_str = '\n'.join(deck_str) + '\n'
        deck_str += str(self.deck)

        # The shop
        shop_str = [
            ' ___ _             ',
            '/ __| |_  ___ _ __ ',
            '\\__ \\ \' \\/ _ \ \'_ \\',
            '|___/_||_\\___/ .__/',
            '             |_|   ',
        ]
        shop_str = '\n'.join(shop_str) + '\n'
        shop_str += str(self.shop)

        # Game over?
        complete_str = ''
        if self.won:
            complete_str = 'You won!'
        elif self.lost:
            complete_str = 'You lost!'
        else:
            complete_str = 'Game ongoing...'

        result = '\n'.join([status, deck_str, shop_str, complete_str])
        return result

    def __call__(self, *args: Any, **kwds: Any):
        """Prints self when called."""
        print(self)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def lives(self) -> int:
        return self._n_lives

    @lives.setter
    @check_game_over
    def lives(self, value: int):
        if type(value) == int:
            self._n_lives = value
        else:
            raise TypeError('lives must be an integer value')

    @property
    def trophies(self) -> int:
        return self._n_trophies

    @trophies.setter
    @check_game_over
    def trophies(self, value: int):
        if type(value) == int:
            self._n_trophies = value
        else:
            raise TypeError('trophies must be an integer value')

    @property
    def gold(self) -> int:
        return self._n_gold

    @gold.setter
    @check_game_over
    def gold(self, value: int):
        if type(value) == int:
            if value < 0:
                raise Warning('gold set to 0')
            self._n_gold = max(0, value)
        else:
            raise TypeError('gold must be an integer value')

    @property
    def display(self) -> bool:
        try:
            return self._display_game
        except:
            raise AttributeError('display has not yet been set')

    @display.setter
    @check_game_over
    def display(self, value: bool):
        if type(value) == bool:
            self._display_game = value
        else:
            raise TypeError('display must be a boolean value')

    @property
    def actions_taken(self):
        return self._n_actions_taken

    @property
    def won(self) -> bool:
        return self.trophies == self._TROPHIES_TO_WIN

    @property
    def lost(self) -> bool:
        return self.lives == 0

    @property
    def game_over(self) -> bool:
        return self.won or self.lost

    @check_game_over
    @display_game
    def roll(self, is_turn_start: bool = False):
        """
        Rolls the shop.

        Parameters
        ----------
        is_turn_start: bool
            If True, the shop is rolled for free. If False (default), the shop
            is rolled only if the player can afford the roll, in which case the
            player loses a gold amount equivalent to the roll cost.

        Examples
        ----------
        Roll the shop upon starting a new game:

        >>> my_game = Game(display=True)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |OTTER     ||ANT       ||SLOTH     ||          ||          ||APPLE     ||          |
        |hp:  2    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |atk: 1    ||atk: 2    ||atk: 1    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> my_game.roll()
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 9  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |CRICKET   ||OTTER     ||SLOTH     ||          ||          ||APPLE     ||          |
        |hp:  2    ||hp:  2    ||hp:  1    ||          ||          ||          ||          |
        |atk: 1    ||atk: 1    ||atk: 1    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        """
        self._n_actions_taken += 1

        if not is_turn_start and self.gold >= self._ROLL_COST:
            self.gold -= self._ROLL_COST
            self.shop.roll()
        elif is_turn_start:
            self.shop.roll()

        for i in range(len(self.shop)):
            if isinstance(self.shop[i].item, Pet):
                self.shop[i].item.assign_game(self)

    @check_game_over
    @display_game
    def freeze(self, index: int):
        """
        Freezes the shop slot at the given index, if non-empty.

        Frozen shop slots have an asterisk next to the name of their contained
        item. When the shop is rolled, frozen slots are guaranteed to be
        unchanged.

        Parameters
        ----------
        index: int
            The index of the shop slot to freeze.

        Examples
        ----------
        Freeze shop slot 0:

        >>> my_game = Game(display=True)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |PIG       ||HORSE     ||ANT       ||          ||          ||APPLE     ||          |
        |hp:  1    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |atk: 3    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> my_game.freeze(0)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |PIG*      ||HORSE     ||ANT       ||          ||          ||APPLE     ||          |
        |hp:  1    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |atk: 3    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        """
        self._n_actions_taken += 1

        item = self.shop[index].item
        is_frozen = self.shop[index].is_frozen
        if item:
            self.shop[index] = ShopItem(item, not is_frozen)

    @check_game_over
    @display_game
    def buy(self, a: int | SrcDstPair, b: Optional[int] = None):
        """
        Buys a shop item and places it into the deck.

        If the player cannot afford the purchase, this is a no-op. If a pet is
        placed onto a pet of the same type that can level, this performs a 
        merge. If the target pet cannot be leveled, this is a no-op. If the
        target pet is not the same type, this is a no-op.

        Parameters
        ----------
        a: int | SrcDstPair
            If integer, the index of the shop slot to purchase from. If
            SrcDstPair, a 2-tuple where the first element is the index
            of the shop slot to purchase from and the second element is the
            index of the deck slot to place into.

        b: int | None
            If a is an integer, the index of the deck slot to place into. If a
            is a SrcDstPair, ignored.

        Examples
        ----------
        Purchase from shop slot 0 and place into deck slot 1:

        >>> my_game = Game(display=True)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |PIG       ||HORSE     ||ANT       ||          ||          ||APPLE     ||          |
        |hp:  1    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |atk: 3    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> my_game.buy(0,1)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 7  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||PIG       ||          |
        |          ||          ||          ||hp:  1    ||          |
        |          ||          ||          ||atk: 3    ||          |
        |          ||          ||          ||fct: ...  ||          |
        |          ||          ||          ||exp: 0/2  ||          |
        |          ||          ||          ||lvl: 1    ||          |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||HORSE     ||ANT       ||          ||          ||APPLE     ||          |
        |          ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |          ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |          ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |          ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |          ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6

        Alternatively:

        >>> my_game.buy((0,1))

        See also
        ----------
        - `gym_snape.game.pets.pet`
        """
        self._n_actions_taken += 1

        if type(a) == tuple and len(a) == 2:
            shop_index, deck_index = a
            if type(shop_index) != int or type(deck_index) != int:
                raise ValueError(
                    'the elements of the SrcDstPair must be integers'
                )
        elif type(a) == int and type(b) == int:
            shop_index, deck_index = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters a and b, or'
                ' just a as a SrcDstPair'
            )

        if self._n_gold >= 3 and self.shop[shop_index].item:
            self.deck[deck_index] = self.shop[shop_index].item
            if self.deck.success:  # check if insertion was successful
                self._n_gold -= self.shop[shop_index].item.gold_cost
                del self.shop[shop_index]
                self.deck[deck_index].on_buy()

    @check_game_over
    @display_game
    def sell(self, index: int):
        """
        Sells the deck item at index.

        If the selected deck slot is empty, this is a no-op. Otherwise, the
        player receives 1 gold per level of the sold pet.

        Parameters
        ----------
        index: int
            The index of the deck slot to sell from.

        Examples
        ---------
        Sell deck slot 0:

        >>> print(my_game)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 7  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||          ||BEAVER    |
        |          ||          ||          ||          ||hp:  2    |
        |          ||          ||          ||          ||atk: 2    |
        |          ||          ||          ||          ||fct: ...  |
        |          ||          ||          ||          ||exp: 0/2  |
        |          ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||PIG       ||ANT       ||          ||          ||APPLE     ||          |
        |          ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |          ||atk: 3    ||atk: 2    ||          ||          ||          ||          |
        |          ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |          ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |          ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6   
        >>> my_game.sell(0)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 8  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
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
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||PIG       ||ANT       ||          ||          ||APPLE     ||          |
        |          ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |          ||atk: 3    ||atk: 2    ||          ||          ||          ||          |
        |          ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |          ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |          ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        """
        self._n_actions_taken += 1

        pet = self.deck[index]
        if pet:
            self._n_gold += pet.gold_cost
            pet.on_sell()
            del self.deck[index]

    @check_game_over
    @display_game
    def swap(self, a: int | SrcDstPair, b: Optional[int] = None):
        """
        Swaps the contents of two deck slots.

        Explicitly does NOT perform a merge, even if the pets contained in the
        two specified slots are of the same type.

        Parameters
        ----------
        a: int | SrcDstPair
            If integer, the source deck slot. If SrcDstPair, a 2-tuple where 
            the first element is the index of the source deck slot and the 
            second element is the index of the destination deck slot.

        b: int | None
            If a is an integer, the index of the deck slot to place into. If a
            is a SrcDstPair, ignored.

        Examples
        ----------
        Move the pet in deck slot 0 to deck slot 2:

        >>> print(my_game)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 5  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||          ||PIG       |
        |          ||          ||          ||          ||hp:  1    |
        |          ||          ||          ||          ||atk: 3    |
        |          ||          ||          ||          ||fct: ...  |
        |          ||          ||          ||          ||exp: 0/2  |
        |          ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||          ||ANT       ||          ||          ||APPLE     ||          |
        |          ||          ||hp:  1    ||          ||          ||          ||          |
        |          ||          ||atk: 2    ||          ||          ||          ||          |
        |          ||          ||fct: ...  ||          ||          ||          ||          |
        |          ||          ||exp: 0/2  ||          ||          ||          ||          |
        |          ||          ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> my_game.swap(0,2)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 5  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||PIG       ||          ||          |
        |          ||          ||hp:  1    ||          ||          |
        |          ||          ||atk: 3    ||          ||          |
        |          ||          ||fct: ...  ||          ||          |
        |          ||          ||exp: 0/2  ||          ||          |
        |          ||          ||lvl: 1    ||          ||          |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||          ||ANT       ||          ||          ||APPLE     ||          |
        |          ||          ||hp:  1    ||          ||          ||          ||          |
        |          ||          ||atk: 2    ||          ||          ||          ||          |
        |          ||          ||fct: ...  ||          ||          ||          ||          |
        |          ||          ||exp: 0/2  ||          ||          ||          ||          |
        |          ||          ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6

        Alternatively:

        >>> my_game.swap((0,2))
        """
        self._n_actions_taken += 1

        if type(a) == tuple and len(a) == 2:
            src, dst = a
            if type(src) != int or type(dst) != int:
                raise ValueError(
                    'the elements of the SrcDstPair must be integers'
                )
        elif type(a) == int and type(b) == int:
            src, dst = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters a and b, or'
                ' just a as a SrcDstPair'
            )

        self.deck.swap(src, dst)

    @check_game_over
    @display_game
    def merge(self, a: int | SrcDstPair, b: Optional[int] = None):
        """
        Merges the contents of two deck slots.

        If the pets contained in the two specified deck slots cannot be merged,
        this is a no-op.

        Parameters
        ----------
        a: int | SrcDstPair
            If integer, the source deck slot. If SrcDstPair, a 2-tuple where 
            the first element is the index of the source deck slot and the 
            second element is the index of the destination deck slot.

        b: int | None
            If a is an integer, the index of the deck slot to merge into. If a
            is a SrcDstPair, ignored.

        Examples
        ----------
        Merge the pet in deck slot 2 into the pet in deck slot 0:
        >>> print(my_game)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 5  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||PIG       ||          ||PIG       |
        |          ||          ||hp:  1    ||          ||hp:  1    |
        |          ||          ||atk: 3    ||          ||atk: 3    |
        |          ||          ||fct: ...  ||          ||fct: ...  |
        |          ||          ||exp: 0/2  ||          ||exp: 0/2  |
        |          ||          ||lvl: 1    ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||          ||ANT       ||          ||          ||APPLE     ||          |
        |          ||          ||hp:  1    ||          ||          ||          ||          |
        |          ||          ||atk: 2    ||          ||          ||          ||          |
        |          ||          ||fct: ...  ||          ||          ||          ||          |
        |          ||          ||exp: 0/2  ||          ||          ||          ||          |
        |          ||          ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> my_game.merge(2,0)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 5  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||          ||PIG       |
        |          ||          ||          ||          ||hp:  2    |
        |          ||          ||          ||          ||atk: 4    |
        |          ||          ||          ||          ||fct: ...  |
        |          ||          ||          ||          ||exp: 1/2  |
        |          ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||          ||ANT       ||          ||          ||APPLE     ||          |
        |          ||          ||hp:  1    ||          ||          ||          ||          |
        |          ||          ||atk: 2    ||          ||          ||          ||          |
        |          ||          ||fct: ...  ||          ||          ||          ||          |
        |          ||          ||exp: 0/2  ||          ||          ||          ||          |
        |          ||          ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6

        Alternatively:

        >>> my_game.merge((2,0))

        See also
        ----------
        - `gym_snape.game.pets.pet`
        """
        self._n_actions_taken += 1

        if type(a) == tuple and len(a) == 2:
            src, dst = a
            if type(src) != int or type(dst) != int:
                raise ValueError(
                    'the elements of the SrcDstPair must be integers'
                )
        elif type(a) == int and type(b) == int:
            src, dst = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters a and b, or'
                ' just a as a SrcDstPair'
            )

        self.deck.merge(src, dst)

    @check_game_over
    def _new_turn(self):
        """
        Resets the player's gold, rolls the shop, and increments turn.

        Called at the end of each battle.
        """
        self.gold = self._GOLD_PER_TURN
        self._turn += 1
        self.shop.turn = self._turn
        self.roll(is_turn_start=True)

    @check_game_over
    def challenge(self, other_game_instance) -> None:
        """
        Challenge another game instance to battle.

        This function modifies the state of both the challenger (the calling
        instance) and the opponent (the parameter instance).

        Parameters
        ----------
        other_game_instance: Game
            The opponent game instance.

        Examples
        ----------
        Player 1 (`p1`) challenges player 2 (`p2`) to a battle:

        >>> print(p1)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 1  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |HORSE     ||          ||          ||          ||ANT       |
        |hp:  1    ||          ||          ||          ||hp:  2    |
        |atk: 2    ||          ||          ||          ||atk: (5)  |
        |fct: ...  ||          ||          ||          ||fct: ...  |
        |exp: 0/2  ||          ||          ||          ||exp: 1/2  |
        |lvl: 1    ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||          ||          ||          ||          ||APPLE     ||          |
        |          ||          ||          ||          ||          ||          ||          |
        |          ||          ||          ||          ||          ||          ||          |
        |          ||          ||          ||          ||          ||          ||          |
        |          ||          ||          ||          ||          ||          ||          |
        |          ||          ||          ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> print(p2)
        +------------------------------------------------+
        | TURN: 1  | LIVES: 10 | TROPHIES: 0  | GOLD: 7  |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||          ||PIG       |
        |          ||          ||          ||          ||hp:  1    |
        |          ||          ||          ||          ||atk: 3    |
        |          ||          ||          ||          ||fct: ...  |
        |          ||          ||          ||          ||exp: 0/2  |
        |          ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |          ||ANT       ||ANT       ||          ||          ||APPLE     ||          |
        |          ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |          ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |          ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |          ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |          ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        >>> p1.challenge(p2)
        __   __
        \\ \\ / /__ _  _
         \\ V / _ \\ || |
          |_|\\___/\\_,_|
        +------------------------------------------------+
        | TURN: 2  | LIVES: 10 | TROPHIES: 1  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |HORSE     ||          ||          ||          ||ANT       |
        |hp:  1    ||          ||          ||          ||hp:  2    |
        |atk: 2    ||          ||          ||          ||atk: 3    |
        |fct: ...  ||          ||          ||          ||fct: ...  |
        |exp: 0/2  ||          ||          ||          ||exp: 1/2  |
        |lvl: 1    ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |MOSQUITO  ||ANT       ||ANT       ||          ||          ||APPLE     ||          |
        |hp:  2    ||hp:  1    ||hp:  1    ||          ||          ||          ||          |
        |atk: 2    ||atk: 2    ||atk: 2    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
         ___
        | __|__  ___
        | _/ _ \\/ -_)
        |_|\\___/\\___|
        +------------------------------------------------+
        | TURN: 2  | LIVES: 9  | TROPHIES: 0  | GOLD: 10 |
        +------------------------------------------------+
         ___         _
        |   \\ ___ __| |__
        | |) / -_) _| / /
        |___/\\___\\__|_\\_\\
        4----------43----------32----------21----------10----------0
        |          ||          ||          ||          ||PIG       |
        |          ||          ||          ||          ||hp:  1    |
        |          ||          ||          ||          ||atk: 3    |
        |          ||          ||          ||          ||fct: ...  |
        |          ||          ||          ||          ||exp: 0/2  |
        |          ||          ||          ||          ||lvl: 1    |
        4----------43----------32----------21----------10----------0
         ___ _
        / __| |_  ___ _ __
        \\__ \\ ' \\/ _ \\ '_ \\
        |___/_||_\\___/ .__/
                     |_|
        0----------01----------12----------23----------34----------45----------56----------6
        |FISH      ||OTTER     ||MOSQUITO  ||          ||          ||APPLE     ||          |
        |hp:  3    ||hp:  2    ||hp:  2    ||          ||          ||          ||          |
        |atk: 2    ||atk: 1    ||atk: 2    ||          ||          ||          ||          |
        |fct: ...  ||fct: ...  ||fct: ...  ||          ||          ||          ||          |
        |exp: 0/2  ||exp: 0/2  ||exp: 0/2  ||          ||          ||          ||          |
        |lvl: 1    ||lvl: 1    ||lvl: 1    ||          ||          ||          ||          |
        0----------01----------12----------23----------34----------45----------56----------6
        """
        # Make copies of each game instance's deck
        my_deck = deepcopy(self.deck)
        their_deck = deepcopy(other_game_instance.deck)

        # Assign enemies to both decks
        for i in range(len(my_deck)):
            if my_deck[i]:
                my_deck[i].assign_enemies(their_deck)
        for i in range(len(their_deck)):
            if their_deck[i]:
                their_deck[i].assign_enemies(my_deck)

        # Ability cast order is highest attack power to lowest attack power
        MY_DECK, THEIR_DECK = 0, 1  # helper constants for the function

        def get_ability_cast_order():
            result = []
            for i, (a, b) in enumerate(zip(my_deck, their_deck)):
                if a:
                    result.append((MY_DECK, i, a))
                if b:
                    result.append((THEIR_DECK, i, b))
            result.sort(key=lambda x: x[-1])
            return result

        # Cast battle start abilities on the battle-copies of both decks
        order = get_ability_cast_order()
        for whose_deck, index, _ in order:
            if whose_deck == MY_DECK:
                my_deck[index].on_battle_start()
            elif whose_deck == THEIR_DECK:
                their_deck[index].on_battle_start()

        # Battle until one or both decks are depleted
        while not my_deck.is_empty() and not their_deck.is_empty():
            order = get_ability_cast_order()
            my_deck.shift_forward()
            their_deck.shift_forward()
            my_first, their_first = my_deck[0], their_deck[0]
            my_deck[0].health -= their_first.attack
            their_deck[0].health -= my_first.attack

        # Assign rewards based on battle result
        if not my_deck.is_empty() and their_deck.is_empty():
            self.trophies += 1
            other_game_instance.lives -= 1
        elif my_deck.is_empty() and not their_deck.is_empty():
            other_game_instance.trophies += 1
            self.lives -= 1

        # Cast battle end abilities on the original copies of both decks
        for my_pet, their_pet in zip(self.deck, other_game_instance.deck):
            if my_pet:
                my_pet.on_battle_end()
            if their_pet:
                their_pet.on_battle_end()

        # Get new turn for challenger
        if self.display:
            challenger_str = [
                '__   __        ',
                '\\ \\ / /__ _  _ ',
                ' \\ V / _ \\ || |',
                '  |_|\\___/\\_,_|'
            ]
            print('\n'.join(challenger_str))
        self._new_turn()

        # Get new turn for foe
        if self.display:
            opponent_str = [
                ' ___         ',
                '| __|__  ___ ',
                '| _/ _ \\/ -_)',
                '|_|\\___/\\___|'
            ]
            print('\n'.join(opponent_str))
        other_game_instance._new_turn()
