"""
Definitions of the tier 5 food items: Chili, Chocolate, and Sushi.
"""

__all__ = ['Chili', 'Chocolate', 'Sushi']

# Local application imports
from gym_snape.game.food import Food

# Third party imports
import numpy as np


class Chili(Food):
    def __init__(self):
        super().__init__()
        self._name = 'CHILI'

    def on_use(self, index):
        """Give a deck pet the Splash Attack effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Spl'
            self._last_op_success = True
        else:
            self._last_op_success = False


class Chocolate(Food):
    def __init__(self):
        super().__init__()
        self._name = 'CHOCOLATE'

    def on_use(self, index):
        """Give a deck pet +1 experience."""
        if self._deck[index]:
            # Get previous experience/level
            prev_exp = self._deck[index].experience
            prev_lvl = self._deck[index].level

            # Increment experience
            self._deck[index].experience += 1

            # Get new experience/level
            new_exp = self._deck[index].experience
            new_lvl = self._deck[index].level

            # Success if either experience or level increased
            self._last_op_success = new_exp > prev_exp or new_lvl > prev_lvl
        else:
            self._last_op_success = False


class Sushi(Food):
    def __init__(self):
        super().__init__()
        self._name = 'SUSHI'
        self.attack = 1
        self.health = 1

    def on_use(self, *args, **kwargs):
        """Give 3 random animals +1/+1."""
        choices = [pet for pet in self._deck if pet]
        n_chosen = min(len(choices), 3)
        if n_chosen >= 1:
            chosen = np.random.choice(choices, n_chosen, replace=False)
            for c in chosen:
                c.attack += self.attack
                c.health += self.health
            self._last_op_success = True
        else:
            self._last_op_success = False
