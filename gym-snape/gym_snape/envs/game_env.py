# Standard library imports
import json
from pathlib import Path

# Third-party imports
import gym
from gym import spaces
import numpy as np
import pandas as pd


class GameEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, config_dir):
        super(GameEnv, self).__init__()

        """
        Read configuration directory files.
        """
        config_dir = Path(config_dir)
        main_config_file = config_dir.joinpath('main.json')
        with open(main_config_file, 'r') as f:
            main_config = json.load(f)

        pets_config_file = config_dir.joinpath('pets.csv')
        pets_config = pd.read_csv(pets_config_file)

        food_config_file = config_dir.joinpath('food.csv')
        food_config = pd.read_csv(food_config_file)

        """
        N = total number of shop slots (empty and non-empty)
        M = total number of deck slots (empty and non-empty)

        From the human POV, game controls can be conceptualized 
        as discrete action spaces:
            (1) Buy from shop: Discrete (N*M)+1
                - N*M pairs of shop slots and deck slots + no-op                
            (2) Sell from deck: Discrete M+1
                - M deck slots + no-op
            (3) Re-order deck: Discrete (M*M)+1
                - M*M pairs of source/destination deck slots + no-op
            (4) End turn: Discrete 2
                - Pressed + no-op
        
        Note that merges are not an explicit action, but can be performed if a
        pet is bought and placed into a slot with the same pet or if the deck
        is re-ordered such that two of the same pets are in the same slot.

        But for an RL agent, it must pick just one action, so actually it 
        should be one discrete space rather than 4 disinct ones. And thus, we 
        don't need a no-op action since there will always be one taken.
        """
        num_shop_slots = main_config['num_shop_slots']
        num_deck_slots = main_config['num_deck_slots']

        # Define the ranges of each sub-action-space
        self.buy_actions = range(num_shop_slots * num_deck_slots)
        self.sell_actions = range(self.buy_actions.stop,
                                  self.buy_actions.stop + num_deck_slots)
        self.reorder_actions = range(self.sell_actions.stop,
                                     self.sell_actions.stop +
                                     np.power(self.deck_slots, 2, dtype=int))
        self.end_turn_action = self.reorder_actions.stop

        # Define the entire action space
        self.action_space = spaces.Discrete(self.end_turn_action)

        """
        N = total number of pets and items, not including empty
        S = number of shop slots
        D = number of deck slots

        Observations can be conceptualized as multiple observation spaces:
            (1) Number of trophies: Discrete
            (2) Amount of gold: Discrete
            (3) Number of hearts: Discrete
            (4) Level number: Discrete
            (5) Shop: MultiDiscrete [(N+1)_1 (N+1)_2 ... (N+1)_S]
            (6) Deck: MultiDiscrete [(N+1)_1 (N+1)_2 ... (N+1)_D]
        """
        num_trophies = main_config['num_trophies']
        num_hearts = main_config['num_hearts']
        max_int = np.iinfo(np.int32).max
        max_obj_id = len(pets_config) + len(food_config)
        self.observation_space = spaces.Dict({
            'num_trophies': spaces.Discrete(num_trophies+1),
            'num_hearts': spaces.Discrete(num_hearts+1),
            'num_gold': spaces.Discrete(max_int),
            'level_num': spaces.Discrete(max_int),
            'shop': spaces.MultiDiscrete([max_obj_id+1] * num_shop_slots),
            'deck': spaces.MultiDiscrete([max_obj_id+1] * num_deck_slots)
        })

        # Initial game state
        self.state = {
            'num_trophies': 0,
            'num_hearts': 10,
            'num_gold': 10,
            'level_num': 0,
            'shop': self.observation_space['shop'].sample(),
            'deck': [0] * num_deck_slots
        }
        # TODO: figure out how to change numbe of shop slots with level,
        # and limit which pets/food are available at each level

        assert self.observation_space.contains(self.state), \
            'Invalid initial state'

    def step(self, action):
        # Process actions
        reward = 0
        assert self.action_space.contains(action)

        if action in self.buy_actions:
            pass
        elif action in self.sell_actions:
            pass
        elif action in self.reorder_actions:
            pass
        elif action == self.end_turn_action:
            pass  # do battle

        observation = self._get_obs()
        done = observation['num_hearts'] == 0
        info = {}

        return observation, reward, done, info

    def reset(self):
        self.state = {
            'num_trophies': 0,
            'num_hearts': 10,
            'num_gold': 10,
            'level_num': 0,
            'shop': self.observation_space['shop'].sample(),
            'deck': [0] * len(self.observation_space['deck'])
        }
        return self._get_obs()

    def _get_obs(self):
        return self.state

    def render(self, mode='human'):
        pass

    def close(self):
        pass
