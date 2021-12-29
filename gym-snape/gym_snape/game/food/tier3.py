"""
Definitions of the tier 3 food items: Garlic and Salad Bowl.
"""

__all__ = ['Garlic', 'SaladBowl']

# Local application imports
from gym_snape.game.food import Food

# Third party imports
import numpy as np


class Garlic(Food):
    def __init__(self):
        super().__init__()
        self._name = 'GARLIC'

    def on_use(self, index):
        """Give a deck pet garlic armor effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Glc'
            self._last_op_success = True
        else:
            self._last_op_success = False


class SaladBowl(Food):
    def __init__(self):
        super().__init__()
        self._name = 'SALAD'
        self.attack = 1
        self.health = 1

    def on_use(self, *args, **kwargs):
        """Give 2 random animals +1/+1."""
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
