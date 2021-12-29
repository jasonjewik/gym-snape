"""
Definitions of the tier 2 food items: Cupcake, Meat Bone, and Sleeping Pill.
"""

__all__ = ['Cupcake', 'MeatBone', 'SleepingPill']

# Local application imports
from gym_snape.game.food import Food


class Cupcake(Food):
    def __init__(self):
        super().__init__()
        self.attack = 3
        self.health = 3
        self._name = 'CUPCAKE'

    def on_use(self, index):
        """Give a deck pet +3/+3 until the end of the battle."""
        if self._deck[index]:
            self._deck[index].attack_buff += self.attack
            self._deck[index].health_buff += self.health
            self._last_op_success = True
        else:
            self._last_op_success = False


class MeatBone(Food):
    def __init__(self):
        super().__init__()
        self._name = 'MEAT BONE'

    def on_use(self, index):
        """Give a deck pet bone attack effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Bne'
            self._last_op_success = True
        else:
            self._last_op_success = False


class SleepingPill(Food):
    def __init__(self):
        super().__init__()
        self._name = 'SLEEPING PILL'
        self._gold_cost = 1

    def on_use(self, index):
        """Make a deck pet faint."""
        if self._deck[index]:
            self._deck[index].faint()
            self._last_op_success = True
        else:
            self._last_op_success = False
