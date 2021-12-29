# Standard library imports
from abc import ABC, abstractmethod
import typing


class Food(ABC):
    """
    The base class for food items. 

    The method `on_use` must be overriden in objects that subclass this.
    A food's name must be at least 3 characters long and these first 3
    characters must be unique among all foods.
    """

    def __init__(self):
        self._name = ''
        self._last_op_success = True
        self._gold_cost = 3
        self._health = 0
        self._attack = 0

    def __str__(self):
        """Returns the name of this food item on a card."""
        width = 10
        border = '+----------+'
        name_row = f'|{self._name[:width]:{width}}|'
        empty_row = ['|          |'] * 5
        result = [border, name_row] + empty_row + [border]
        result = '\n'.join(result)
        return result

    @property
    def id(self):
        """
        Returns the concatenated integer representations of the first 3
        chars of the food's name.
        """
        return int(''.join([str(ord(ch)) for ch in self._name[:3]]))

    @property
    def success(self):
        return self._last_op_success

    @property
    def gold_cost(self):
        return self._gold_cost

    @gold_cost.setter
    def gold_cost(self, value: int):
        if type(value) != int:
            raise TypeError('gold cost must be integer value')
        elif value < 0:
            raise Warning('negative gold cost set to 0')
        self._gold_cost = max(0, value)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        if type(value) != int:
            raise TypeError('health must be integer value')
        else:
            self._health = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value: int):
        if type(value) != int:
            raise TypeError('attack must be integer value')
        else:
            self._attack = value

    @abstractmethod
    def on_use(self, *args, **kwargs):
        """What happens when the food is used. Must set `_last_op_success`."""
        raise NotImplementedError

    @typing.final
    def assign_deck(self, value):
        """Assigns a deck to this food item."""
        self._deck = value

    @typing.final
    def assign_shop(self, value):
        """Assigns a shop to this food item."""
        self._shop = value
