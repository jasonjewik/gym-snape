"""
Definitions of the tier 1 pets: Ant, Beaver, Cricket, Fish, Horse, Mosquito, 
Otter, Pig, and Sloth.
"""

__all__ = ['Ant', 'Beaver', 'Cricket', 'Fish', 'Horse', 'Mosquito', 'Otter',
           'Pig', 'Sloth']

# Local application imports
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens
from gym_snape.game.pets.pet import capture_action, duplicate_action

# Third party imports
import numpy as np


class Ant(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'ANT'
        self.attack = 2
        self.health = 1

    @capture_action
    def on_faint(self):
        """Give a random friend +(2*level) attack, +(1*level) health."""
        super().on_faint()
        choices = []
        for friend in self._friends:
            if friend and id(friend) != id(self):
                choices.append(friend)
        if len(choices) >= 1:
            chosen = np.random.choice(choices, replace=False)
            chosen.attack += 2 * self.level
            chosen.health += 1 * self.level


class Beaver(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'BEAVER'
        self.attack = 2
        self.health = 2

    def on_sell(self):
        """Give 2 random friends +(1*level) health."""
        super().on_sell()
        choices = []
        for friend in self._friends:
            if friend and id(friend) != id(self):
                choices.append(friend)
        n_chosen = min(len(choices), 2)
        if n_chosen >= 1:
            chosen = np.random.choice(choices, n_chosen, replace=False)
            for c in chosen:
                c.health += 1 * self.level


class Cricket(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'CRICKET'
        self.attack = 1
        self.health = 2

    @capture_action
    def on_faint(self):
        """Summon a Zombie Cricket."""
        i = self._friends.index(self)
        zombie = tokens.ZombieCricket(self)
        super().on_faint()
        self._friends.insert(i, zombie)


class Fish(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'FISH'
        self.attack = 2
        self.health = 3

    def on_level_up(self):
        """Give all friends +(1*level) attack, +(1*level) health."""
        super().on_level_up()
        for friend in self._friends:
            if friend and id(friend) != id(self):
                friend.health += 1 * self.level
                friend.attack += 1 * self.level


class Horse(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'HORSE'
        self.attack = 2
        self.health = 1

    @capture_action
    def on_friend_summoned(self, index):
        """Give the friend +1 attack until end of battle."""
        if self._friends[index] and id(self._friends[index]) != id(self):
            super().on_friend_summoned(index)
            self._friends[index].attack_buff += 1


class Mosquito(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'MOSQUITO'
        self.attack = 2
        self.health = 2

    @capture_action
    def on_battle_start(self):
        """Deal 1 damage to (1*level) random enemies."""
        super().on_battle_start()
        choices = [enemy for enemy in self._enemies if enemy]
        n_chosen = min(len(choices), self.level)
        if n_chosen >= 1:
            enemies = np.random.choice(choices, n_chosen, replace=False)
            for enemy in enemies:
                enemy.health -= 1 * self.level


class Otter(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'OTTER'
        self.attack = 1
        self.health = 2

    def on_buy(self):
        """Give a random friend +(1*level) health, +(1*level) attack."""
        super().on_buy()
        choices = []
        for friend in self._friends:
            if friend and id(friend) != id(self):
                choices.append(friend)
        n_chosen = min(len(choices), self.level)
        if n_chosen >= 1:
            friend = np.random.choice(choices)
            friend.health += 1 * self.level
            friend.attack += 1 * self.level


class Pig(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'PIG'
        self.attack = 3
        self.health = 1

    def on_sell(self):
        """Gain +(1*level) gold."""
        super().on_sell()
        self._game.gold += 1 * self.level


class Sloth(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SLOTH'
        self.attack = 1
        self.health = 1
