"""
Definitions of the tier 6 food items: Melon, Mushroom, Pizza, and Steak.
"""

__all__ = ['Melon', 'Mushroom', 'Pizza', 'Steak']

# Local application imports
from gym_snape.game.food import Food

# Third party imports
import numpy as np


class Melon(Food):
    def __init__(self):
        super().__init__()
        self._name = 'MELON'

    def on_use(self, index):
        """Gives a deck pet the melon armor effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Mln'
            self._last_op_success = True
        else:
            self._last_op_success = False


class Mushroom(Food):
    def __init__(self):
        super().__init__()
        self._name = 'MUSHROOM'

    def on_use(self, index):
        """Gives a deck pet the extra life effect."""
        if self._deck[index]:
            self._deck[index].effect = '1up'
            self._last_op_success = True
        else:
            self._last_op_success = False


class Pizza(Food):
    def __init__(self):
        super().__init__()
        self._name = 'PIZZA'
        self.attack = 2
        self.health = 2

    def on_use(self, *args, **kwargs):
        """Give 2 random animals +2/+2."""
        choices = [pet for pet in self._deck if pet]
        n_chosen = min(len(choices), 2)
        if n_chosen >= 1:
            chosen = np.random.choice(choices, n_chosen, replace=False)
            for c in chosen:
                c.attack += self.attack
                c.health += self.health
            self._last_op_success = True
        else:
            self._last_op_success = False


class Steak(Food):
    def __init__(self):
        super().__init__()
        self._name = 'STEAK'

    def on_use(self, index):
        """Give an animal the Steak Attack effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Stk'
            self._last_op_success = True
        else:
            self._last_op_success = False
