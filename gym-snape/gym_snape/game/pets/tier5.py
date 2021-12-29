"""
Definitions for the tier 5 pets: Cow, Crocodile, Monkey, Rhino, Scorpion,
Seal, Shark, Turkey.
"""

__all__ = ['Cow', 'Crocodile', 'Monkey', 'Rhino', 'Scorpion', 'Seal', 'Shark',
           'Turkey']

# Local application imports
from gym_snape.game.food import Food
from gym_snape.game.food.misc import Milk
from gym_snape.game.pets import Pet
from gym_snape.game.shop import ShopItem
from gym_snape.game.pets.pet import capture_action, duplicate_action

# Third party imports
import numpy as np


class Cow(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'COW'
        self.attack = 4
        self.health = 6

    def on_buy(self):
        """Replace current shop items with milk."""
        super().on_buy()
        for i in range(len(self._shop)):
            if isinstance(self._shop[i].item, Food):
                self._shop[i] = ShopItem(item=Milk(self), is_frozen=False)


class Crocodile(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'CROCODILE'
        self.attack = 8
        self.health = 4

    @capture_action
    def on_battle_start(self):
        """Deal 8*level damage to the last enemy."""
        super().on_battle_start()
        i = len(self._enemies) - 1
        while i > 0:
            if self._enemies[i]:
                self._enemies[i].health -= 8 * self.level
                break
            i -= 1


class Monkey(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'MONKEY'
        self.attack = 1
        self.health = 2

    def on_turn_end(self):
        """Give rightmost friend +(3*level)/+(3*level)."""
        super().on_turn_end()
        i = 0
        while i < len(self._friends):
            if self._friends[i]:
                self._friends[i].attack += 3 * self.level
                self._friends[i].health += 3 * self.level
                break
            i += 1


class Rhino(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'RHINO'
        self.attack = 5
        self.health = 8

    @capture_action
    def on_knock_out(self):
        """Deal (4*level) damage to the first enemy."""
        super().on_knock_out()
        i = 0
        while i < len(self._enemies):
            if self._enemies[i]:
                self._enemies[i].health -= 4 * self.level
                break
            i += 1


class Scorpion(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SCORPION'
        self.attack = 1
        self.health = 1
        self.effect = 'Psn'


class Seal(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SEAL'
        self.attack = 3
        self.health = 8

    def on_eat_food(self):
        """Give 2 random friends +(1*level)/+(1*level)."""
        choices = []
        for friend in self._friends:
            if friend and id(friend) != id(self):
                choices.append(friend)
        n_choices = min(len(choices), 2)
        if n_choices >= 1:
            chosen = np.random.choice(choices, n_choices, replace=False)
            for c in chosen:
                c.health += 1 * self.level
                c.attack += 1 * self.level


class Shark(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SHARK'
        self.attack = 4
        self.health = 4

    @capture_action
    def on_friend_faint(self, *args, **kwargs):
        """Gain +(2*level)/+(1*level)."""
        self.health += 2 * self.level
        self.attack += 1 * self.level


class Turkey(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'TURKEY'
        self.attack = 3
        self.health = 4

    @capture_action
    def on_friend_summoned(self, index):
        """Give the friend +(3*level)/+(3*level)."""
        if id(self._friends[index]) != id(self):
            super().on_friend_summoned(index)
            self._friends[index].attack += 3 * self.level
            self._friends[index].health += 3 * self.level
