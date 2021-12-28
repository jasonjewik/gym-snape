"""
Definitions of the tier 1 food items: Apple and Honey. Also defines each food
item's roll chance.
"""

# Local application imports
from gym_snape.game.food import Food


class Apple(Food):
    def __init__(self):
        super().__init__()
        self._name = 'APPLE'

    def on_use(self, index):
        """Give a deck pet +1 attack, +1 health."""
        if self._deck[index]:
            self._deck[index].attack += 1
            self._deck[index].health += 1
            self._last_op_success = True
        else:
            self._last_op_success = False


class Honey(Food):
    def __init__(self):
        super().__init__()
        self._name = 'HONEY'

    def on_use(self, index):
        """Give a deck pet the Honey Bee effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Bee'
            self._last_op_success = True
        else:
            self._last_op_success = False


ROLL_CHANCES = {
    Apple: 1/2,
    Honey: 1/2
}
