"""
Definitions of the tier 1 pets: Ant, Beaver, Cricket, Fish, Horse, Mosquito, 
Otter, Pig, and Sloth. Also defines each pet's roll chance.
"""

# Local application imports
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens

# Third party imports
import numpy as np


class Ant(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 1
        self._name = 'ANT'

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 2
        self._name = 'BEAVER'

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 2
        self._name = 'CRICKET'

    def on_faint(self):
        """Summon a Zombie Cricket."""
        super().on_faint()
        for i in range(len(self._friends)):
            if id(self._friends[i]) == id(self):
                del self._friends[i]
                self._friends[i] = tokens.ZombieCricket(self)


class Fish(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 3
        self._name = 'FISH'

    def on_level_up(self):
        """Give all friends +(1*level) attack, +(1*level) health."""
        super().on_level_up()
        for friend in self._friends:
            if friend and id(friend) != id(self):
                friend.health += 1 * self.level
                friend.attack += 1 * self.level


class Horse(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 1
        self._name = 'HORSE'

    def on_friend_summoned(self, index):
        """Give the friend +1 attack until end of battle."""
        if id(self._friends[index]) != id(self):
            super().on_friend_summoned(index)
            self._friends[index].attack_buff += 1


class Mosquito(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 2
        self._name = 'MOSQUITO'

    def on_battle_start(self):
        """Deal 1 damage to (1*level) random enemies."""
        super().on_battle_start()
        choices = [enemy for enemy in self._enemies if enemy]
        n_chosen = min(len(choices), self.level)
        if n_chosen >= 1:
            enemies = np.random.choice(choices, n_chosen, replace=False)
            for enemy in enemies:
                enemy.health += 1 * self.level


class Otter(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 2
        self._name = 'OTTER'

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 3
        self.health = 1
        self._name = 'PIG'

    def on_sell(self):
        """Gain +(1*level) gold."""
        super().on_sell()
        self._game.gold += 1 * self.level


class Sloth(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 1
        self._name = 'SLOTH'


ROLL_CHANCES = {
    Ant: 1/9,
    Beaver: 1/9,
    Cricket: 1/9,
    Fish: 1/9,
    Horse: 1/9,
    Mosquito: 1/9,
    Otter: 1/9,
    Pig: 1/9,
    Sloth: 1/9
}
