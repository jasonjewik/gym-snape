"""
Definitions of the tier 3 pets: Badger, Blowfish, Camel, Dog, Giraffe,
Kangaroo, Ox, Rabbit, Sheep, Snail, Turtle.
"""

__all__ = ['Badger', 'BlowFish', 'Camel', 'Dog', 'Giraffe', 'Kangaroo',
           'Ox', 'Rabbit', 'Sheep', 'Snail', 'Turtle']

# Local application imports
from gym_snape.game.game import MatchResult
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens
from gym_snape.game.pets.pet import capture_action, duplicate_action

# Third party imports
import numpy as np


class Badger(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'BADGER'
        self.attack = 5
        self.health = 4

    @duplicate_action
    def on_faint(self):
        """Deal attack*level damage to adjacent pets."""
        damage = self.attack * self.level
        i = self._friends.index(self)

        # Deal damage to friend directly behind (if exists)
        behind = i + 1
        if behind < len(self._friends) and self._friends[behind]:
            self._friends[behind].health -= damage

        # Deal damage to friend directly ahead (if exists)
        ahead = i - 1
        if ahead >= 0 and self._friends[ahead]:
            self._friends[ahead].health -= damage
        # If at front of deck, deal damage to enemy in first slot (if exists)
        elif ahead == -1 and self._enemies[0]:
            self._enemies[0].health -= damage

        super().on_faint()


class BlowFish(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'BLOWFISH'
        self.attack = 3
        self.health = 5

    @capture_action
    @duplicate_action
    def on_hurt(self):
        """Deal 2*level damage to a random enemy."""
        super().on_hurt()
        choices = [enemy for enemy in self._enemies if enemy]
        n_chosen = min(len(choices), 1)
        if n_chosen == 1:
            chosen = np.random.choice(choices, n_chosen, replace=False)
            for c in chosen:
                c.health -= 2 * self.level


class Camel(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'CAMEL'
        self.attack = 2
        self.health = 5

    @capture_action
    @duplicate_action
    def on_hurt(self):
        """Give friend behind +(1*level) attack, +(2*level) health."""
        super().on_hurt()
        i = self._game.index(self) + 1
        while i < len(self._game):
            if self._game[i]:
                self._game[i].attack += 1 * self.level
                self._game[i].health += 2 * self.level
                break


class Dog(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DOG'
        self.attack = 2
        self.health = 2

    @duplicate_action
    def on_friend_summoned(self, *args, **kwargs):
        """Gain +(1*level) health or attack (temporary if in battle)."""
        super().on_friend_summoned()
        coin_flip = np.random.randint(2)
        if coin_flip == 0:
            self.health += 1 * self.level
        else:
            self.attack += 1 * self.level


class Giraffe(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'GIRAFFE'
        self.attack = 2
        self.health = 5

    @capture_action
    def on_turn_end(self):
        """Give 1/2/3 friends ahead +1/+1."""
        super().on_turn_end()
        i = self._friends.index(self) - 1
        count = 0
        while i > 0 and count < self.level:
            if self._friends[i]:
                self._friends[i].attack += 1
                self._friends[i].health += 1
                count += 1
            i -= 1


class Kangaroo(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'KANGAROO'
        self.attack = 1
        self.health = 2

    @capture_action
    @duplicate_action
    def on_friend_attack(self, index):
        """Friend ahead attacks: gain +(2*level) attack and health."""
        super().on_friend_attack()
        i = self._friends.index(self)
        # Check that there are no pets in between
        if index > i:
            return
        else:
            i -= 1
            in_between = False
            while i > index:
                if self._friends[i]:
                    in_between = True
                i -= 1
            if not in_between and i == index:
                self.health += 2 * self.level
                self.attack += 2 * self.level


class Ox(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'OX '  # pet names must be at least 3 chars
        self.attack = 1
        self.health = 4

    @capture_action
    @duplicate_action
    def on_friend_faint(self, friend_index):
        """Friend ahead faints: gain melon armor and +(2*level) attack."""
        my_index = self._friends.index(self)
        if friend_index > my_index:  # do nothing, if friend was behind
            return
        else:  # check that there are no pets in between
            i = my_index
            pet_between = False
            while i > friend_index:
                if self._friends[i]:
                    pet_between = True
                i -= 1
            if not pet_between:
                self.effect = 'Mln'
                self.attack += 2 * self.level


class Rabbit(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'RABBIT'
        self.attack = 3
        self.health = 2

    @capture_action
    def on_friend_eat_food(self, index):
        """Give the friend +(1*level) health."""
        super().on_friend_eat_food()
        self._friends[index].health += 1 * self.level


class Sheep(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SHEEP'
        self.attack = 2
        self.health = 2

    @duplicate_action
    def on_faint(self):
        """Summon two (2*level)/(2*level) Rams."""
        super().on_faint()
        index = self._friends.index(self)
        self._friends.insert(index, tokens.Ram(self))
        self._friends.insert(index, tokens.Ram(self))


class Snail(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SNAIL'
        self.attack = 2
        self.health = 2

    @capture_action
    def on_buy(self):
        """Give all friends +(2*level)/+(1*level), if last battle was lost."""
        super().on_buy()
        if self._game.match_history[-1] == MatchResult.LOST:
            for i in range(len(self._friends)):
                if self._friends[i] and id(self._friends[i]) != id(self):
                    self._friends[i].attack += 2 * self.level
                    self._friends[i].health += 1 * self.level


class Turtle(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'TURTLE'
        self.attack = 1
        self.health = 2

    @duplicate_action
    def on_faint(self):
        """Gives 1/2/3 friends behind Melon Armor effect."""
        super().on_faint()
        i = self._friends.index(self) + 1
        num_affected = 0
        while i < len(self._friends) and num_affected < self.level:
            if self._friends[i]:
                self._friends[i]._effect = 'Mln'
                num_affected += 1
