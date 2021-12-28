# Standard library imports
from abc import ABC, abstractmethod
import typing


class Food(ABC):
    """
    The base class for food items. 

    The method `on_use` must be overriden in objects that subclass this.
    """

    def __init__(self):
        self._last_op_success = True
        self._gold_cost = 3

    def __str__(self):
        """Returns the name of this food item on a card."""
        width = 10
        border = '+----------+'
        name_row = f'|{self._name:{width}}|'
        empty_row = ['|          |'] * 5
        result = [border, name_row] + empty_row + [border]
        result = '\n'.join(result)
        return result

    @property
    def success(self):
        return self._last_op_success

    @property
    def gold_cost(self):
        return self._gold_cost

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
