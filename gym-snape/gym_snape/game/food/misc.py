"""
Defines miscellaneous foods that cannot be rolled for in the shop.
"""

__all__ = ['Milk']

# Local application imports
from gym_snape.game.food import Food


class Milk(Food):
    def __init__(self, parent):
        super().__init__()
        self._name = 'MILK'
        self.attack = 1 * parent.level
        self.health = 2 * parent.level
        self._gold_cost = 0

    def on_use(self, index):
        """Give a deck pet +1 attack, +2 health, scaling with the level of the
        cow that summoned this."""
        if self._deck[index]:
            self._deck[index].attack += self.attack
            self._deck[index].health += self.health
            self._last_op_success = True
        else:
            self._last_op_success = False
