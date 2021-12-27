from typing import OrderedDict
from gym_snape.game.pets import tier1 as tier1_pets
from gym_snape.game.food import tier1 as tier1_food
from gym_snape.game.pets.pet import Pet
from gym_snape.game.food.food import Food
import numpy as np
from collections import namedtuple

ShopItem = namedtuple('ShopItem',
                      field_names=['item', 'is_frozen'],
                      defaults=[None, False])


class Shop:
    def __init__(self):
        self._turn = 1

        self._n_pets_at_turn = dict([(1, 3), (3, 3), (5, 4), (9, 5)])
        self._n_pet_slots = self._n_pets_at_turn[self.turn]
        self._n_food_at_turn = dict([(1, 1), (3, 2)])
        self._n_food_slots = self._n_food_at_turn[self.turn]

        max_pet_slots = self._n_pets_at_turn[max(self._n_pets_at_turn.keys())]
        max_food_slots = self._n_food_at_turn[max(self._n_food_at_turn.keys())]
        self._pet_slots = [ShopItem()] * max_pet_slots
        self._food_slots = [ShopItem()] * max_food_slots

        self._avail_tiers_at_turn = dict([(1, 1), (3, 2), (5, 3), (7, 4),
                                          (9, 5), (11, 6)])
        self._highest_avail_tier = self._avail_tiers_at_turn[self.turn]

        self._all_pets = {
            1: tier1_pets.ROLL_CHANCES
        }

        self._all_food = {
            1: tier1_food.ROLL_CHANCES
        }

        self.rng = np.random.default_rng()

    def __getitem__(self, index):
        if index < len(self._pet_slots):
            return self._pet_slots[index]
        else:
            index -= len(self._pet_slots)
            return self._food_slots[index]

    def __setitem__(self, index, value):
        assert type(value) == ShopItem, \
            f'shop item must be a named tuple of the form {ShopItem.__doc__}'
        if index < len(self._pet_slots) and isinstance(value.item, Pet):
            self._pet_slots[index] = value
        else:
            index -= len(self._pet_slots)
            if isinstance(value.item, Food):
                self._food_slots[index] = value

    def __delitem__(self, index):
        if index < len(self._pet_slots):
            self._pet_slots[index] = ShopItem()
        else:
            index -= len(self._pet_slots)
            self._food_slots[index] = ShopItem()

    def __len__(self):
        return len(self._pet_slots) + len(self._food_slots)

    def __str__(self):
        substrs = []
        for i, (item, is_frozen) in enumerate(self):
            if item:
                item_str_arr = str(item).replace('+', str(i)).split('\n')
                if is_frozen:
                    item_str_arr[1] = item_str_arr[1].replace(' ', '*', 1)
                item_str_arr = [i + '\n' for i in item_str_arr]
                substrs.append(item_str_arr)
            else:
                border = f'{i}----------{i}\n'
                rows = ['|          |\n'] * 6
                substrs.append([border] + rows + [border])
        result = ''
        for _ in range(8):
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
    def turn(self, value):
        self._turn = value
        self._n_pet_slots = self._n_pets_at_turn.get(
            self.turn, self._n_pet_slots)
        self._n_food_slots = self._n_food_at_turn.get(
            self.turn, self._n_food_slots)
        self._highest_avail_tier = self._avail_tiers_at_turn.get(
            self.turn, self._highest_avail_tier)

    def roll(self):
        avail_pets = []
        avail_food = []
        pet_roll_probs = []
        food_roll_probs = []
        for t in range(1, self._highest_avail_tier+1):
            avail_pets.extend(self._all_pets[t].keys())
            avail_food.extend(self._all_food[t].keys())
            pet_roll_probs.extend(self._all_pets[t].values())
            food_roll_probs.extend(self._all_food[t].values())
        pet_roll_probs = np.array(pet_roll_probs) / self._highest_avail_tier
        food_roll_probs = np.array(food_roll_probs) / self._highest_avail_tier

        pets = self.rng.choice(
            avail_pets,
            size=self._n_pet_slots,
            replace=True,
            p=pet_roll_probs
        )
        for i, p in enumerate(pets):
            if not self._pet_slots[i].is_frozen:
                self._pet_slots[i] = ShopItem(p(), False)

        food = self.rng.choice(
            avail_food,
            size=self._n_food_slots,
            replace=True,
            p=food_roll_probs
        )
        for i, f, in enumerate(food):
            if not self._food_slots[i].is_frozen:
                self._food_slots[i] = ShopItem(f(), False)
