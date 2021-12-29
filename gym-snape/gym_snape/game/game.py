# Standard library imports
from copy import deepcopy
from functools import wraps
from collections.abc import Callable
from typing import Any, Final, List, Optional, ParamSpec, Tuple, TypeVar

# Local application imports
from gym_snape.game.utils import MatchResult
from gym_snape.game.deck import Deck
from gym_snape.game.pets import Pet
from gym_snape.game.shop import Shop, ShopItem

# Typing definitions
P = ParamSpec('P')
T = TypeVar('T')
SrcDstPair = Tuple[int, int]
AbilityCastEntry = Tuple[Pet, Callable[P, T], Any, Any]


def display_game(bound_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Game`'s methods that prints the state of the game after
    the decorated method is called."""
    @wraps(bound_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        result = bound_method(self, *args, **kwargs)
        if self.display:
            print(self)
        return result
    return _impl


def check_game_over(bound_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Game`'s methods that turns each method into a no-op
    once a game over (win or loss) is detected."""
    @wraps(bound_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        if not self.game_over:
            result = bound_method(self, *args, **kwargs)
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
        self._match_history = []
        self.roll(is_turn_start=True)

        self._abilities_to_cast = []

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

    @property
    def match_history(self) -> List[MatchResult]:
        return self._match_history

    @check_game_over
    def add_ability_to_cast(self, value: AbilityCastEntry):
        """
        Adds an ability to be cast at the next turn of the battle.

        Parameters
        ----------
        value: AbilityCastEntry
            This is a 4-tuple. The first element is the Pet requesting to cast
            an ability. The second element is the ability to be cast. The third
            and fourth elements are args and kwargs, respectively.
        """
        if type(value) == tuple:
            if len(value) == 4:
                if isinstance(value[0], Pet):
                    self._abilities_to_cast.append(value)
                else:
                    raise ValueError('the first element should be a Pet')
            else:
                raise ValueError('value should only have four elements')
        else:
            raise TypeError('value must be of type AbilityCastEntry')

    @check_game_over
    def cast_all_abilities(self, other_game_instance):
        """
        Casts friendly and enemy abilities in order of the pets' attack power,
        from greatest first to least last.

        Parameters
        ----------
        other_game_instance: Game
            The game instance with the enemy deck.
        """
        # Merge and sort
        a2c = self._abilities_to_cast + other_game_instance._abilities_to_cast
        a2c.sort(key=lambda x: x[0], reverse=True)

        # Cast abilities
        for a in a2c:
            pet, ability, args, kwargs = a
            ability(pet, *args, **kwargs)

        # Clear all abilities
        self._abilities_to_cast = []
        other_game_instance._abilities_to_cast = []

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
                print(self.shop[i].item._game)

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

        item = self.shop[shop_index].item
        if item and self._n_gold >= item.gold_cost:
            self.deck[deck_index] = self.shop[shop_index].item
            if self.deck.success:  # check if insertion was successful
                self._n_gold -= self.shop[shop_index].item.gold_cost
                del self.shop[shop_index]
                if self.deck[deck_index]:
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

        # Sell the specified pet
        pet = self.deck[index]
        if pet:
            self._n_gold += pet.gold_cost
            pet.on_sell()
            del self.deck[index]

            # Trigger on friend sold abilities
            for remaining_pet in self.deck:
                if remaining_pet:
                    remaining_pet.on_friend_sold()

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
        # Reset gold
        self.gold = self._GOLD_PER_TURN

        # Increment turn and roll shop
        self._turn += 1
        self.shop.turn = self._turn
        self.roll(is_turn_start=True)

        # Call on turn start
        for i in range(len(self.deck)):
            if self.deck[i]:
                self.deck[i].on_turn_start()

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
        # Tell each pet they are now in battle
        for pet in self.deck:
            if pet:
                pet.in_battle = True
        for pet in other_game_instance.deck:
            if pet:
                pet.in_battle = True

        print('Begin battle')

        # Call on turn end for the pets
        for pet in self.deck:
            if pet:
                pet.on_turn_end()
        for pet in other_game_instance.deck:
            if pet:
                pet.on_turn_end()
        self.cast_all_abilities(other_game_instance)

        print('Called end turn')

        # Make copies of each game instance's deck
        my_deck = deepcopy(self.deck)
        their_deck = deepcopy(other_game_instance.deck)

        # Assign enemies to both decks
        for i, pet in enumerate(my_deck):
            if pet:
                pet.assign_enemies(their_deck)
                print(f'my enemies {i}\n', pet._enemies)
        for i, pet in enumerate(their_deck):
            if pet:
                pet.assign_enemies(my_deck)
                print(f'their enemies {i}\n', pet._enemies)

        print('Assigned enemies')

        # Call on battle start for the pets
        for pet in self.deck:
            if pet:
                pet.on_battle_start()
        for pet in other_game_instance.deck:
            if pet:
                pet.on_battle_start()
        self.cast_all_abilities(other_game_instance)

        print('Called on battle start')

        # Battle until one or both decks are depleted
        while not my_deck.is_empty() and not their_deck.is_empty():
            print(my_deck)
            print(their_deck)

            # Push pets toward each other
            my_deck.shift_all_forward()
            their_deck.shift_all_forward()

            # Cast before attack abilities
            my_deck[0].before_attack()
            their_deck[0].before_attack()
            self.cast_all_abilities(other_game_instance)

            print('Called before attack abilities')

            # Determine damage to leading pets
            my_first, their_first = my_deck[0], their_deck[0]
            damage_to_me = their_first.attack
            damage_to_them = my_first.attack

            # Determine splash damage
            my_splash = 5 if my_first.effect == 'Spl' else 0
            their_splash = 5 if their_first.effect == 'Spl' else 0

            # Leading pets hit each other "simultaneously"
            my_deck[0].health -= damage_to_me
            their_deck[0].health -= damage_to_them

            # Apply poison damage
            if my_first.effect == 'Psn' and their_deck[0].health < their_first.health:
                their_deck[0].faint()
            if their_first.effect == 'Psn' and my_deck[0].health < my_first.health:
                my_deck[0].faint()

            # Splash damage is applied
            if my_deck[1]:
                my_deck[1].health -= their_splash
            if their_deck[1]:
                their_deck[1].health -= my_splash

            # Cast any on hurt and faint abilities
            self.cast_all_abilities(other_game_instance)

            print('Cast on hurt and faint abilities')

            # Cast on knock out abilities
            if my_deck[0] is None:
                for pet in their_deck:
                    if pet:
                        pet.on_knock_out()
            if their_deck[0] is None:
                for pet in my_deck:
                    if pet:
                        pet.on_knock_out()
            self.cast_all_abilities(other_game_instance)

            print('Cast knock out abilities')

            # Cast on friend attack abilities
            for pet in my_deck:
                if pet:
                    pet.on_friend_attack(0)
            for pet in their_deck:
                if pet:
                    pet.on_friend_attack(0)
            self.cast_all_abilities(other_game_instance)

            print('Cast on friend attacked abilities')

        print('Battle concluded')

        # Assign rewards based on battle result
        if not my_deck.is_empty() and their_deck.is_empty():
            self.trophies += 1
            other_game_instance.lives -= 1
            self._match_history.append(MatchResult.WON)
        elif my_deck.is_empty() and not their_deck.is_empty():
            other_game_instance.trophies += 1
            self.lives -= 1
            self._match_history.append(MatchResult.LOST)
        else:
            self._match_history.append(MatchResult.DRAW)

        # Cast battle end abilities on the original copies of both decks
        for pet in self.deck:
            if pet:
                pet.on_battle_end()
                pet.in_battle = False
        for pet in other_game_instance.deck:
            if pet:
                pet.on_battle_end()
                pet.in_battle = False
        self.cast_all_abilities(other_game_instance)

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
