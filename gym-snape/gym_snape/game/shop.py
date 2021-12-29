# Standard library imports
from collections import namedtuple
from typing import Literal

# Local application imports
from gym_snape.game import pets, food
from gym_snape.game.pets.pet import Pet
from gym_snape.game.food.food import Food

# Third party imports
import numpy as np


# Definition of a helper tuple for the Shop class
ShopItem = namedtuple('ShopItem',
                      field_names=['item', 'is_frozen'],
                      defaults=[None, False])


class Shop:
    """
    The shop used in the game.

    The number of pet/food slots increases with turn number, as does the tier
    of available pets/food.
    """

    def __init__(self):
        self._turn = 1

        # Maps turn numbers to the number of pet shop slots available starting
        # that turn (e.g., 3 slots at turn 1)
        self._n_pets_at_turn = dict([(1, 3), (3, 3), (5, 4), (9, 5)])
        self._n_pet_slots = self._n_pets_at_turn[self.turn]

        # Maps turn numbers to the number of food shop slots available starting
        # that turn (e.g., 1 slot at turn 1)
        self._n_food_at_turn = dict([(1, 1), (3, 2)])
        self._n_food_slots = self._n_food_at_turn[self.turn]

        # Maps turn numbers to the highest available tier starting that turn
        # (e.g, tier 2 pets/food become availale at turn 3)
        self._avail_tiers_at_turn = dict([(1, 1), (3, 2), (5, 3), (7, 4),
                                          (9, 5), (11, 6)])
        self._highest_avail_tier = self._avail_tiers_at_turn[self.turn]

        # The lists that actually represent the shop slots
        max_pet_slots = self._n_pets_at_turn[max(self._n_pets_at_turn.keys())]
        max_food_slots = self._n_food_at_turn[max(self._n_food_at_turn.keys())]
        self._pet_slots = [ShopItem()] * max_pet_slots
        self._food_slots = [ShopItem()] * max_food_slots

        # Shop pet modifiers
        self._pet_attack_bonus = 0
        self._pet_health_bonus = 0

        # Shop food modifiers
        self._food_attack_multiplier = 1
        self._food_health_multiplier = 1

        # Used for rolling the shop
        self._pet_roll_rates = pets.roll_rates
        self._food_roll_rates = food.roll_rates
        self.rng = np.random.default_rng()

    def __getitem__(self, index: int) -> ShopItem:
        if index < len(self._pet_slots):
            return self._pet_slots[index]
        else:
            index -= len(self._pet_slots)
            return self._food_slots[index]

    def __setitem__(self, index: int, value: ShopItem):
        if type(value) == ShopItem:
            if index < len(self._pet_slots) and isinstance(value.item, Pet):
                self._pet_slots[index] = value
            else:
                index -= len(self._pet_slots)
                if isinstance(value.item, Food):
                    self._food_slots[index] = value
                    self._food_slots[index].item.assign_shop(self)
        else:
            raise TypeError(
                f'shop item must be of the form {ShopItem.__doc__}'
            )

    def __delitem__(self, index: int):
        """Sets the shop slot at the given index to None."""
        if index < len(self._pet_slots):
            self._pet_slots[index] = ShopItem()
        else:
            index -= len(self._pet_slots)
            self._food_slots[index] = ShopItem()

    def __len__(self) -> Literal[7]:
        """Returns the total number of pet and food slots (7, by default)."""
        return len(self._pet_slots) + len(self._food_slots)

    def __str__(self):
        """
        Returns the state of the shop as a set of cards.
        """
        # Get the string representation of each individual slot
        substrs = []
        for i, (item, is_frozen) in enumerate(self):
            if item:  # representation for a filled slot
                # Put the index of the shop slot in the corner of the card
                item_str_arr = str(item).replace('+', str(i)).split('\n')
                if is_frozen:  # mark frozen slots with an asterisk
                    name_row = item_str_arr[1]
                    item_str_arr[1] = name_row[:-2] + '*' + '|'
                item_str_arr = [i + '\n' for i in item_str_arr]
                substrs.append(item_str_arr)
            else:  # representation for the empty slot (None)
                border = f'{i}----------{i}\n'
                rows = ['|          |\n'] * 6
                substrs.append([border] + rows + [border])

        # Put the cards together by attaching the ends of each line
        result = ''
        for _ in range(len(substrs[0])):
            for i in range(len(substrs)):
                if i == len(substrs) - 1:
                    result += substrs[i].pop(0)
                else:
                    result += substrs[i].pop(0).strip()
        result = result.strip()
        return result

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value: int):
        if type(value) != int:
            raise TypeError('turn must be an integer value')
        else:
            # Update the number of pet/food slots and highest available tier
            self._turn = value
            self._n_pet_slots = self._n_pets_at_turn.get(
                self.turn, self._n_pet_slots)
            self._n_food_slots = self._n_food_at_turn.get(
                self.turn, self._n_food_slots)
            self._highest_avail_tier = self._avail_tiers_at_turn.get(
                self.turn, self._highest_avail_tier)

    @property
    def tier(self):
        return self._highest_avail_tier

    @property
    def pet_attack_bonus(self):
        return self._pet_attack_bonus

    @pet_attack_bonus.setter
    def pet_attack_bonus(self, value: int):
        if type(value) != int:
            raise TypeError('pet attack bonus must be an integer value')
        else:
            self._pet_attack_bonus = value

    @property
    def pet_health_bonus(self):
        return self._pet_health_bonus

    @pet_health_bonus.setter
    def pet_health_bonus(self, value: int):
        if type(value) != int:
            raise TypeError('pet health bonus must be an integer value')
        else:
            self._pet_health_bonus = value

    @property
    def food_attack_multiplier(self):
        return self._food_attack_multiplier

    @food_attack_multiplier.setter
    def food_attack_multiplier(self, value: int):
        if type(value) != int:
            raise TypeError('food attack multiplier must be an integer value')
        elif value <= 0:
            raise ValueError('food attack multiplier must be positive')
        else:
            self._food_attack_multiplier = value

    @property
    def food_health_multiplier(self):
        return self._food_health_multiplier

    @food_health_multiplier.setter
    def food_health_multiplier(self, value: int):
        if type(value) != int:
            raise TypeError('food health multiplier must be an integer value')
        elif value <= 0:
            raise ValueError('food health multiplier must be positive')
        else:
            self._food_health_multiplier = value

    def apply_pet_bonuses(self):
        """Applies health and attack bonuses to current shop pets."""
        for i in range(len(self._pet_slots)):
            if self._pet_slots[i].item:
                self._pet_slots[i].item.attack += self.pet_attack_bonus
                self._pet_slots[i].item.health += self.pet_health_bonus

    def apply_food_multipliers(self):
        """Applies health and attack multipliers to current shop food."""
        for i in range(len(self._food_slots)):
            if self._food_slots[i].item:
                self._food_slots[i].item.attack *= self._food_attack_multiplier
                self._food_slots[i].item.health *= self._food_health_multiplier

    def roll(self):
        """
        Rolls the shop, ignoring frozen slots.

        Examples
        ----------
        See the docstring for `game.Game.roll`
        """
        # Pick and set pets into non-frozen slots
        avail_pets, pet_roll_probs = [], []
        for rr in self._pet_roll_rates[self._highest_avail_tier]:
            avail_pets.append(rr.item)
            pet_roll_probs.append(rr.rate)
        pets = self.rng.choice(
            avail_pets,
            size=self._n_pet_slots,
            replace=True,
            p=pet_roll_probs
        )
        for i, p in enumerate(pets):
            if not self._pet_slots[i].is_frozen:
                pet = p()
                pet.assign_shop(self)
                self._pet_slots[i] = ShopItem(pet, False)

        # Pick and set food items into non-frozen slots
        avail_food, food_roll_probs = [], []
        for rr in self._food_roll_rates[self._highest_avail_tier]:
            avail_food.append(rr.item)
            food_roll_probs.append(rr.rate)
        food = self.rng.choice(
            avail_food,
            size=self._n_food_slots,
            replace=True,
            p=food_roll_probs
        )
        for i, f, in enumerate(food):
            if not self._food_slots[i].is_frozen:
                food = f()
                food.assign_shop(self)
                self._food_slots[i] = ShopItem(food, False)

        # Apply modifiers
        self.apply_pet_bonuses()
        self.apply_food_multipliers()
