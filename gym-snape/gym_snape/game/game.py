from functools import wraps
from copy import deepcopy

from gym_snape.game.pets.pet import Pet
from gym_snape.game.deck import Deck
from gym_snape.game.shop import Shop, ShopItem


def _debug_print(class_method):
    @wraps(class_method)
    def _impl(self, *args, **kwargs):
        result = class_method(self, *args, **kwargs)
        if self.debug:
            print(self)
        return result
    return _impl


class Game:
    def __init__(self, debug=False):
        self.deck = Deck()
        self.shop = Shop()

        self._turn = 1
        self._n_lives = 10
        self._n_trophies = 0
        self._trophies_to_win = 10
        self._n_gold = 10
        self._gold_per_turn = 10

        self._roll_cost = 3
        self._purchase_value = 3
        self._resale_value = 1  # per level

        self.debug = debug
        self.roll(is_turn_start=True)

    def __str__(self):
        """ASCII art courtesy of https://patorjk.com/software/taag/."""

        width = 2
        status = ' | '.join([
            f'TURN: {self._turn:{width}}',
            f'LIVES: {self._n_lives:{width}}',
            f'TROPHIES: {self._n_trophies:{width}}',
            f'GOLD: {self._n_gold:{width}}'
        ])
        status = '| ' + status + ' |\n'
        border = '+' + '-' * (len(status) - 3) + '+\n'
        status = border + status + border.strip()

        deck_str = [
            ' ___         _   ',
            '|   \ ___ __| |__',
            '| |) / -_) _| / /',
            '|___/\___\__|_\_\\'
        ]
        deck_str = '\n'.join(deck_str) + '\n'
        deck_str += str(self.deck)

        shop_str = [
            ' ___ _             ',
            '/ __| |_  ___ _ __ ',
            '\__ \ \' \/ _ \ \'_ \\',
            '|___/_||_\___/ .__/',
            '             |_| '
        ]
        shop_str = '\n'.join(shop_str) + '\n'
        shop_str += str(self.shop)

        return status + '\n' + deck_str + '\n' + shop_str

    @property
    def debug(self):
        return self._debug

    @property
    def trophies(self):
        return self._n_trophies

    @trophies.setter
    def trophies(self, value):
        self._n_trophies = value

    @property
    def lives(self):
        return self._n_lives

    @lives.setter
    def lives(self, value):
        self._n_lives = value

    @property
    def gold(self):
        return self._n_gold

    @gold.setter
    def gold(self, value):
        self._n_gold = max(0, value)

    @property
    def won(self):
        return self.trophies == self._trophies_to_win

    @property
    def lost(self):
        return self.lives == 0

    @property
    def game_over(self):
        return self.won or self.lost

    @debug.setter
    def debug(self, value):
        assert type(value) == bool
        self._debug = value

    def new_turn(self):
        self.gold = self._gold_per_turn
        self._turn += 1
        self.shop.turn = self._turn
        self.roll(is_turn_start=True)

    @_debug_print
    def roll(self, is_turn_start=False):
        if not is_turn_start and self.gold >= self._purchase_value:
            self.gold -= self._roll_cost
            self.shop.roll()
        elif is_turn_start:
            self.shop.roll()

        for i in range(len(self.shop)):
            if isinstance(self.shop[i].item, Pet):
                self.shop[i].item.assign_game(self)

    @_debug_print
    def freeze(self, index):
        item = self.shop[index].item
        is_frozen = self.shop[index].is_frozen
        if item:
            self.shop[index] = ShopItem(item, not is_frozen)

    @_debug_print
    def buy(self, a=None, b=None):
        if type(a) == tuple and len(a) == 2:
            shop_index, deck_index = a
            assert type(shop_index) == int and type(deck_index) == int
        elif type(a) == int and type(b) == int:
            shop_index, deck_index = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters shop_index and'
                ' deck_index, or the 2-tuple parameter indices'
            )

        if self._n_gold >= 3:
            self.deck[deck_index] = self.shop[shop_index].item
            if self.deck.success:
                del self.shop[shop_index]
                self._n_gold -= 3
            self.deck[deck_index].on_buy()

    @_debug_print
    def sell(self, index):
        pet = self.deck[index]
        if pet:
            self._n_gold += self._resale_value * pet.level
            pet.on_sell()
            del self.deck[index]

    @_debug_print
    def swap(self, a=None, b=None):
        if type(a) == tuple and len(a) == 2:
            src, dst = a
            assert type(src) == int, type(dst) == int
        elif type(a) == int and type(b) == int:
            src, dst = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters source and'
                ' destination, or the 2-tuple parameter indices'
            )

        self.deck.swap(a, b)

    @_debug_print
    def merge(self, a=None, b=None):
        if type(a) == tuple and len(a) == 2:
            src, dst = a
            assert type(src) == int, type(dst) == int
        elif type(a) == int and type(b) == int:
            src, dst = a, b
        else:
            raise ValueError(
                'exclusively specify either the integer parameters source and'
                ' destination, or the 2-tuple parameter indices'
            )

        self.deck.merge(a, b)

    def challenge(self, other_game_instance):
        MY_DECK, THEIR_DECK = 0, 1

        my_deck = deepcopy(self.deck)
        their_deck = deepcopy(other_game_instance.deck)

        for i in range(len(my_deck)):
            if my_deck[i]:
                my_deck[i].assign_enemies(their_deck)
        for i in range(len(their_deck)):
            if their_deck[i]:
                their_deck[i].assign_enemies(my_deck)

        def get_ability_cast_order():
            result = []
            for i, (a, b) in enumerate(zip(my_deck, their_deck)):
                if a:
                    result.append((MY_DECK, i, a))
                if b:
                    result.append((THEIR_DECK, i, b))
            result.sort(key=lambda x: x[-1])
            return result

        order = get_ability_cast_order()
        for whose_deck, index, _ in order:
            if whose_deck == MY_DECK:
                my_deck[index].on_battle_start()
            elif whose_deck == THEIR_DECK:
                their_deck[index].on_battle_start()

        while not my_deck.is_empty() and not their_deck.is_empty():
            order = get_ability_cast_order()
            my_deck.shift_forward()
            their_deck.shift_forward()
            my_first, their_first = my_deck[0], their_deck[0]
            my_deck[0].health -= their_first.attack
            their_deck[0].health -= my_first.attack

        if not my_deck.is_empty() and their_deck.is_empty():
            self.trophies += 1
            other_game_instance.lives -= 1
        elif my_deck.is_empty() and not their_deck.is_empty():
            other_game_instance.trophies += 1
            self.lives -= 1

        for my_pet, their_pet in zip(self.deck, other_game_instance.deck):
            if my_pet:
                my_pet.on_battle_end()
            if their_pet:
                their_pet.on_battle_end()

        challenger_str = [
            '__   __        ',
            '\ \ / /__ _  _ ',
            ' \ V / _ \ || |',
            '  |_|\___/\_,_|'
        ]
        print('\n'.join(challenger_str))
        self.new_turn()

        opponent_str = [
            ' ___         ',
            '| __|__  ___ ',
            '| _/ _ \/ -_)',
            '|_|\___/\___|'
        ]
        print('\n'.join(opponent_str))
        other_game_instance.new_turn()
