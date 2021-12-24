from gym_snape.game.pets import tier1 as tier1_pets
import numpy as np


class Shop:
    def __init__(self):
        self.turn = 1

        self._n_pets_at_turn = dict([(1, 3), (3, 3), (5, 4), (9, 5)])
        self._n_pet_slots = self._n_pets_at_turn[self.turn]
        self._n_food_at_turn = dict([(1, 1), (3, 2)])
        self._n_food_slots = self._n_pets_at_turn[self.turn]

        max_pet_slots = self._n_pets_at_turn[max(self._n_pets_at_turn.keys())]
        max_food_slots = self._n_food_at_turn[max(self._n_food_at_turn.keys())]
        self._pet_slots = [None] * max_pet_slots
        self._food_slots = [None] * max_food_slots

        self._avail_tiers_at_turn = dict([(1, 1), (3, 2), (5, 3), (7, 4),
                                          (9, 5), (11, 6)])
        self._highest_avail_tier = self._avail_tiers_at_turn[self.turn]

        self._all_pets = {
            1: tier1_pets.ROLL_CHANCES
        }

        self.rng = np.random.default_rng()
        self.roll()

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
        for t in range(self._highest_avail_tier):
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
            self._pet_slots[i] = p

        food = self.rng.choice(
            avail_food,
            size=self._n_food_slots,
            replace=True,
            p=food_roll_probs
        )
        for i, f, in enumerate(food):
            self._food_slots[i] = f
