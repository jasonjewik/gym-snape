"""
Definitions of the tier 4 pets: Bison, Deer, Dolphin, Hippo, Parrot, Penguin,
Rooster, Skunk, Squirrel, Whale and Worm.
"""

__all__ = ['Bison', 'Deer', 'Dolphin', 'Hippo', 'Parrot', 'Penguin', 'Rooster',
           'Skunk', 'Squirrel', 'Whale', 'Worm']

# Standard library imports
from copy import deepcopy
import math

# Local application imports
from gym_snape.game.food import Food
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens
from gym_snape.game.pets.pet import capture_action, duplicate_action


class Bison(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'BISON'
        self.attack = 6
        self.health = 6

    def on_turn_end(self):
        """If there is at least 1 level 3 friend, gain +2/+2."""
        super().on_turn_end()
        for pet in self._friends:
            if pet and pet.level == 3:
                self.attack += 2
                self.health += 2
                break


class Deer(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DEER'
        self.attack = 1
        self.health = 1

    @capture_action
    def on_faint(self):
        """Summon a (5*level)/(5*level) Bus."""
        i = self._friends.index(self)
        bus = tokens.Bus(self)
        super().on_faint()
        self._friends.insert(i, bus)


class Dolphin(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DOLPHIN'
        self.attack = 4
        self.health = 6

    @capture_action
    def on_battle_start(self):
        """Deal 5*level damage to the lowest health enemy."""
        super().on_battle_start()
        lowest_health = self._MAX_HEALTH
        target = -1
        for i in range(len(self._enemies)):
            pet = self._enemies[i]
            if pet and pet.health < lowest_health:
                lowest_health = pet.health
                target = i
        if target != -1:
            self._enemies[target].health -= 5 * self.level


class Hippo(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'HIPPO'
        self.attack = 4
        self.health = 7

    @capture_action
    def on_knock_out(self):
        """Gain +(2*level)/+(2*level)."""
        super().on_knock_out()
        self.attack += 2 * self.level
        self.health += 2 * self.level


class Parrot(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'PARROT'
        self.attack = 5
        self.health = 3

    def on_turn_end(self):
        """Copy ability from friend ahead as a level 1/2/3 until end of battle."""
        super().on_turn_end()

        # Find the friend ahead
        i = self._friends.index(self) - 1
        friend_ahead = None
        while i > 0 and friend_ahead is None:
            if self._friends[i]:
                friend_ahead = deepcopy(self._friends[i])
            i -= 1

        if friend_ahead:
            # Set the friend's level to equal own level
            friend_ahead._level = self.level
            # Set the friend's health and attack to own health/attack
            friend_ahead.zombify(self.health, self.attack)
            # Change friend's name
            friend_ahead._name = self._name

            # Replace self with friend
            del self._friends[i]
            self._friends.insert(i, friend_ahead)


class Penguin(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'PENGUIN'
        self.attack = 1
        self.health = 2

    @capture_action
    def on_turn_end(self):
        """Give all level 2 and 3 friends +(1*level)/+(1*level)."""
        super().on_turn_end()
        for i in range(len(self._friends)):
            if (self._friends[i] and
                    id(self._friends[i]) != id(self) and
                    self._friends[i].level >= 2):
                self._friends[i].attack += 1 * self.level
                self._friends[i].health += 1 * self.level


class Rooster(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'ROOSTER'
        self.attack = 5
        self.health = 3

    @capture_action
    def on_faint(self):
        """Summon 1/2/3 chicks with 1 health and half attack."""
        chicks = []
        for _ in range(self.level):
            chicks.append(tokens.Chick(self))
        i = self._friends.index(self)
        super().on_faint()
        for c in chicks:
            self._friends.insert(i, c)


class Skunk(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SKUNK'
        self.attack = 3
        self.health = 6

    @capture_action
    def on_battle_start(self):
        """Reduce HP of highest health enemy by 33/66/99%."""
        super().on_battle_start()
        highest_health = 0
        target = -1
        for i in range(len(self._enemies)):
            pet = self._enemies[i]
            if pet and pet.health > highest_health:
                highest_health = pet.health
                target = i
        if target != -1:
            ability_modifier = 0.33 * self.level
            new_health = self._enemies[target].health * ability_modifier
            new_health = math.ceil(new_health)
            self._enemies[target]._health = new_health


class Squirrel(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SQUIRREL'
        self.attack = 2
        self.health = 5

    def on_turn_start(self):
        """Discount current shop food by (1*level) gold."""
        super().on_turn_start()
        for i in range(len(self._shop)):
            if isinstance(self._shop[i].item, Food):
                self._shop[i].item.gold_cost -= 1 * self.level


class Whale(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'WHALE'
        self.attack = 2
        self.health = 6
        self._swallowed = None

    @capture_action
    def on_battle_start(self):
        """Swallow friend ahead, triggering their on faint ability."""
        super().on_battle_start()
        i = self._friends.index(self) - 1
        while i > 0 and self._swallowed is None:
            if self._friends[i]:
                self._swallowed = deepcopy(self._friends[i])
                self._friends[i].faint()
            i -= 1

    @capture_action
    def on_faint(self):
        """Release swallowed friend as same level as self."""
        i = self._friends.index(self)
        if self._swallowed:
            self._swallowed.__init__()
            self._swallowed._level = self.level
            self._swallowed.assign_friends(self._friends)
            self._swallowed.assign_enemies(self._enemies)
            super().on_faint()
            self._friends.insert(i, self._swallowed)


class Worm(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'WORM'
        self.attack = 2
        self.health = 2

    def on_eat_food(self):
        """Gain +(1*level)/+(1*level)."""
        super().on_eat_food()
        self.attack += 1 * self.level
        self.health += 1 * self.level
