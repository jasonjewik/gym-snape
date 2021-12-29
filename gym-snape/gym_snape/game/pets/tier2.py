"""
Definitions of the tier 2 pets: Crab, Dodo, Elephant, Flamingo, Hedgehog,
Peacock, Rat, Shrimp, Spider, and Swan.
"""

__all__ = ['Crab', 'Dodo', 'Elephant', 'Flamingo', 'Hedgehog', 'Peacock',
           'Rat', 'Shrimp', 'Spider', 'Swan']

# Local application imports
import math

# Local application imports
from gym_snape.game import pets
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens
from gym_snape.game.pets.pet import capture_action, duplicate_action

# Third party imports
import numpy as np


class Crab(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'CRAB'
        self.attack = 3
        self.health = 3

    @capture_action
    def on_buy(self):
        """Copy the health of the healthiest friend."""
        super().on_buy()
        health = max([f.health for f in self._friends if f])
        self.health = health


class Dodo(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DODO'
        self.attack = 2
        self.health = 3

    @capture_action
    @duplicate_action
    def on_battle_start(self):
        """Give attack to friend ahead, scaling with level."""
        i = self._friends.index(self) - 1
        ability_modifier = self.level / 2
        bonus_attack = math.floor(self.attack * ability_modifier)
        while i > 0:
            if self._friends[i]:
                self._friends[i].attack += bonus_attack
                break
            i -= 1
        super().on_battle_start()


class Elephant(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'ELEPHANT'
        self.attack = 3
        self.health = 5

    @capture_action
    @duplicate_action
    def before_attack(self):
        """Deal 1 damage to 1/2/3 friends behind."""
        super().before_attack()
        i = self._friends.index(self) + 1
        friends_hit = 0
        while i < len(self._friends) and friends_hit < self.level:
            if self._friends[i]:
                self._friends[i].health -= 1
                friends_hit += 1
            else:
                i += 1


class Flamingo(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'FLAMINGO'
        self.attack = 3
        self.health = 1

    @duplicate_action
    def on_faint(self):
        """Give the two friends directly behind +(1*level)/+(1*level)."""
        i = self._friends.index(self) + 1
        stop = i + 2
        while i < len(self._friends) and i < stop:
            if self._friends[i]:
                self._friends[i].attack += 1 * self.level
                self._friends[i].health += 1 * self.level
            i += 1
        super().on_faint()


class Hedgehog(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'HEDGEHOG'
        self.attack = 3
        self.health = 2

    @duplicate_action
    def on_faint(self):
        """Deal 2*level damage to all."""
        for i in range(len(self._friends)):
            if self._friends[i]:
                self._friends[i].health -= 2 * self.level
        for i in range(len(self._enemies)):
            if self._enemies[i]:
                self._enemies[i].health -= 2 * self.level
        super().on_faint()


class Peacock(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'PEACOCK'
        self.attack = 1
        self.health = 5

    @capture_action
    @duplicate_action
    def on_hurt(self):
        """Gain 2*level attack."""
        super().on_hurt()
        self.attack += 2 * self.level


class Rat(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'RAT'
        self.attack = 4
        self.health = 5

    @duplicate_action
    def on_faint(self):
        """Summon a dirty rat on the enemy team."""
        super().on_faint()
        self._enemies.append(tokens.DirtyRat())


class Shrimp(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SHRIMP'
        self.attack = 2
        self.health = 3

    @capture_action
    def on_friend_sold(self):
        """Give a random friend +(1*level) health."""
        super().on_friend_sold()
        choices = []
        for friend in self._friends:
            if friend and id(friend) != id(self):
                choices.append(friend)
        n_chosen = min(len(choices), 1)
        if n_chosen == 1:
            chosen = np.random.choice(choices, n_chosen, replace=False)
            for c in chosen:
                c.health += 1 * self.level


class Spider(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SPIDER'
        self.attack = 2
        self.health = 2

    @duplicate_action
    def on_faint(self):
        """Summon a level 1/2/3 tier 3 pet as a 2/2."""
        i = self._friends.index(self)
        super().on_faint()
        choices = [
            pets.tier3.Badger,
            pets.tier3.BlowFish,
            pets.tier3.Camel,
            pets.tier3.Dog,
            pets.tier3.Giraffe,
            pets.tier3.Kangaroo,
            pets.tier3.Ox,
            pets.tier3.Rabbit,
            pets.tier3.Sheep,
            pets.tier3.Snail,
            pets.tier3.Turtle
        ]
        spawn = np.random.choice(choices, 1)[0]()
        spawn.zombify(2, 2)
        spawn._level = self.level
        self._friends.insert(i, spawn)


class Swan(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SWAN'
        self.attack = 3
        self.health = 3

    @capture_action
    def on_turn_start(self):
        """Gain +(1*level) gold."""
        self._game.gold += 1 * self.level
