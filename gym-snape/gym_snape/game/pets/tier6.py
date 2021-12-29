"""
Definitions for the tier 6 pets: Boar, Cat, Dragon, Fly, Gorilla, Leopard,
Mammoth, Snake and Tiger.
"""

__all__ = ['Boar', 'Cat', 'Dragon', 'Fly', 'Gorilla', 'Leopard', 'Mammoth',
           'Snake', 'Tiger']

# Local application imports
from gym_snape.game import pets
from gym_snape.game.pets import Pet
from gym_snape.game.pets import tokens
from gym_snape.game.pets.pet import capture_action, duplicate_action

# Third party imports
import numpy as np


class Boar(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'BOAR'
        self.attack = 8
        self.health = 6

    @capture_action
    def before_attack(self):
        """Gain +(2*level)/+(2*level)."""
        super().before_attack()
        self.attack += 2 * self.level
        self.health += 2 * self.level


class Cat(Pet):
    def __init__(self):
        """Multiplies the health and attack effect of food by 2/3/4."""
        super().__init__()
        self._name = 'CAT'
        self.attack = 4
        self.health = 5

    def _modify_shop_food(self):
        fam = self._shop.food_attack_multiplier
        self._shop.food_attack_multiplier = max(fam, self.level+1)
        fhm = self._shop.food_health_multiplier
        self._shop.food_health_multiplier = max(fhm, self.level+1)

    def _reset_shop_modifiers(self):
        self._shop.food_attack_multiplier = 1
        self._shop.food_health_multiplier = 1

    def on_buy(self):
        super().on_buy()
        self._modify_shop_food()

    def on_level_up(self):
        super().on_level_up()
        self._modify_shop_food()

    def on_sell(self):
        super().on_sell()
        self._reset_shop_modifiers()
        # Trigger other cats' abilities, if they exist
        for friend in self._friends:
            if friend and type(friend) == type(self) and id(friend) != id(self):
                friend._modify_shop_food()

    def on_faint(self):
        super().on_faint()
        if not self.in_battle:
            self._reset_shop_modifiers()
            # Trigger other cats' abilities, if they exist
            for friend in self._friends:
                if friend and type(friend) == type(self) and id(friend) != id(self):
                    friend._modify_shop_food()


class Dragon(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DRAGON'
        self.attack = 6
        self.health = 8

    def on_friend_bought(self, index):
        """Give all pets +(1*level)/+(1*level) if a tier 1 friend is bought."""
        super().on_friend_bought()
        friend = self._friends[index]
        tier1_pets = list(map(lambda x: x.lower(), dir(pets.tier1)))
        if friend._name.lower() in tier1_pets:
            for i in range(len(self._friends)):
                self._friends[i].health += 1 * self.level
                self._friends[i].attack += 1 * self.level


class Fly(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'FLY'
        self.attack = 5
        self.health = 5
        self._triggers = 3

    def on_battle_start(self):
        super().on_battle_start()
        self._triggers = 3

    @capture_action
    def on_friend_faint(self, index):
        """
        Summon a (5*level)/(5*level) Zombie Fly in place of fainted friend.

        Triggers 3 times per battle. Immune to duplication.
        """
        super().on_friend_faint()
        if self._triggers > 0:
            self._friends.insert(index, tokens.ZombieFly(self))
            self._triggers -= 1


class Gorilla(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'GORILLA'
        self.attack = 6
        self.health = 9
        self._triggers = self.level

    def on_battle_start(self):
        super().on_battle_start()
        self._triggers = self.level

    @capture_action
    def on_hurt(self):
        """Gain Coconut Shield 1/2/3 times per battle."""
        super().on_hurt()
        if self._triggers > 0:
            self.effect = 'Cct'
            self._triggers -= 1


class Leopard(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'LEOPARD'
        self.attack = 10
        self.health = 4

    @capture_action
    def on_battle_start(self):
        """Deal 50% attack to 1/2/3 enemies."""
        super().on_battle_start()
        choices = [e for e in self._enemies if e]
        n_chosen = min(len(choices), self.level)
        if n_chosen >= 1:
            for c in choices:
                c.health -= self.attack // 2


class Mammoth(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'MAMMOTH'
        self.attack = 3
        self.health = 10

    @capture_action
    def on_faint(self):
        """Give all friends +(2*level)/+(2*level)."""
        super().on_faint()
        for f in self._friends:
            if f:
                f.health += 2 * self.level
                f.attack += 2 * self.level


class Snake(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'SNAKE'
        self.attack = 6
        self.health = 6

    @capture_action
    def on_friend_attack(self, index):
        """Deal (5*level) damage to a random enemy when friend ahead attacks."""
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
                choices = [enemy for enemy in self._enemies if enemy]
                if len(choices) >= 1:
                    enemies = np.random.choice(choices, 1, replace=False)
                    for enemy in enemies:
                        enemy.health -= 5 * self.level


class Tiger(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'TIGER'
        self.attack = 4
        self.health = 3

    def on_battle_start(self):
        i = self._friends.index(self)
        while i > 0:
            if self._friends[i]:
                self._friends[i].duplicate_as = self.level
                break
            i -= 1
