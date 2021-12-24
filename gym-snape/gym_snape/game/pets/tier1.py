from gym_snape.game.pets.pet import Pet
from gym_snape.game.pets import tokens
import numpy as np


class Ant(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 1

    def on_faint(self):
        """Give a random friend +(2*level) attack, +(1*level) health."""
        choices = [i for i in range(len(self._deck)) if self._deck[i]]
        index = np.random.choice(choices)
        self._deck[index].attack += 2 * self.level
        self._deck[index].health += 1 * self.level


class Beaver(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 2

    def on_sell(self):
        """Give 2 random friends +(1*level) health."""
        choices = [i for i in range(len(self._deck)) if self._deck[i]]
        indices = np.random.choice(choices, 2)
        for i in indices:
            self._deck[i].health += 1 * self.level


class Cricket(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 2

    def on_faint(self):
        """Summon a Zombie Cricket."""
        for i in range(len(self._deck)):
            if self._deck[i] == self:
                del self._deck[i]
                self._deck[i] = tokens.ZombieCricket(self)


class Fish(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 3

    def on_level_up(self):
        """Give all friends +(1*level) attack, +(1*level) health."""
        for friend in self._deck:
            if friend is not None and friend != self:
                friend.health += 1 * self.level
                friend.attack += 1 * self.level


class Horse(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 1

    def on_friend_summoned(self):
        """Give the friend +1 attack until end of battle."""
        pass


class Mosquito(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 2
        self.health = 2

    def on_battle_start(self):
        """Deal 1 damage to (1*level) random enemies."""
        pass


class Otter(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 2

    def on_buy(self):
        """Give a random friend +(1*level) health, +(1*level) attack."""
        choices = [i for i in range(len(self._deck)) if self._deck[i]]
        index = np.random.choice(choices)
        self._deck[index].health += 1 * self.level
        self._deck[index].attack += 1 * self.level


class Pig(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 3
        self.health = 1

    def on_sell(self):
        """Gain +(1*level) gold."""
        pass


class Sloth(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = 1
        self.health = 1


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
