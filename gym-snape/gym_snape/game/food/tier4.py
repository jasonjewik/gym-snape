"""
Definitions of the tier 4 food items: Canned Food and Pear.
"""

__all__ = ['CannedFood', 'Pear']

# Local application imports
from gym_snape.game.food import Food


class CannedFood(Food):
    def __init__(self):
        super().__init__()
        self._name = 'CANNED FOOD'
        self.attack = 2
        self.health = 2

    def on_use(self, *args, **kwargs):
        """Give all current and future shop pets +2/+2."""
        self._shop.pet_attack_bonus += self.attack
        self._shop.pet_health_bonus += self.health
        self._shop.apply_pet_bonuses()
        self._last_op_success = True


class Pear(Food):
    def __init__(self):
        super().__init__()
        self._name = 'PEAR'
        self.attack = 2
        self.health = 2

    def on_use(self, index):
        """Give a deck pet +2/+2."""
        if self._deck[index] is not None:
            self._deck[index].health += self.attack
            self._deck[index].attack += self.health
            self._last_op_success = True
        else:
            self._last_op_success = False
