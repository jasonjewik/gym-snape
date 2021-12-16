# Standard library imports
import json
from pathlib import Path
from tabulate import tabulate

# Third-party imports
import gym
from gym import spaces
import numpy as np
import pandas as pd


class GameEnv(gym.Env):
    metadata = {'render.modes': ['ansi']}

    def __init__(self, config: str = 'configs/default'):
        super(GameEnv, self).__init__()

        """
        Read configuration directory files.
        """
        config_dir = Path(config)
        main_config_file = config_dir.joinpath('main.json')
        with open(main_config_file, 'r') as f:
            self.main_config = json.load(f)

        pets_config_file = config_dir.joinpath('pets.csv')
        self.pets_config = pd.read_csv(pets_config_file)

        food_config_file = config_dir.joinpath('food.csv')
        self.food_config = pd.read_csv(food_config_file, quotechar='"')

        """
        Validate the configuration files.
        """
        default_config = Path('configs/default')
        default_pet_csv = pd.read_csv(default_config.joinpath('pets.csv'))
        default_food_csv = pd.read_csv(default_config.joinpath('food.csv'),
                                       quotechar='"')

        # Check for required columns
        req_pet_cols = default_pet_csv.columns
        req_food_cols = default_food_csv.columns
        missing_pet_cols = set(self.pets_config.columns) - set(req_pet_cols)
        missing_food_cols = set(self.food_config.columns) - set(req_food_cols)
        assert len(missing_pet_cols) == 0, \
            f'Missing columns {missing_pet_cols} from pet config'
        assert len(missing_food_cols) == 0, \
            f'Missing columns {missing_food_cols} from food config'

        # Check for specification of "empty"
        self.EMPTY_ID = 0
        empty_pet = default_pet_csv.loc[self.EMPTY_ID]
        empty_food = default_food_csv.loc[self.EMPTY_ID]
        assert (self.pets_config.loc[self.EMPTY_ID] == empty_pet).all(), \
            f'Pets config must specify the "empty" pet in the first row:\n{empty_pet}'
        assert (self.food_config.loc[self.EMPTY_ID] == empty_food).all(), \
            f'Food config must specify the "empty" food in the first row:\n{empty_food}'

        """
        N = total number of shop slots (empty and non-empty)
        M = total number of deck slots (empty and non-empty)

        From the human POV, game controls can be conceptualized as discrete
        action spaces:
            (1) Buy from shop: Discrete (N*M)+1
                - N*M pairs of shop slots and deck slots + no-op
            (2) Freeze shop slot: Discrete N+1
                - N slots + no-op
            (3) Re-roll shop: Discrete 2
                - Pressed + no-op
            (4) Sell from deck: Discrete M+1
                - M deck slots + no-op
            (5) Re-order deck: Discrete (M*M)+1
                - M*M pairs of source/destination deck slots + no-op
            (6) End turn: Discrete 2
                - Pressed + no-op

        Note that merges are not an explicit action, but can be performed if a
        pet is bought and placed into a slot with the same pet or if the deck
        is re-ordered such that two of the same pets are in the same slot.

        Since we want an agent to take exactly one action at a time, we can
        combine all these sub-spaces into one large discrete action space. This
        also removes the need for no-op actions.

        So the entire action space will be:
        Discrete (N*M)+(N)+(1)+(M)+(M*M)+(1)
        """
        n_pets, n_food = self.main_config['n_shop_slots'].values()
        n_shop_slots = n_pets + n_food
        n_deck_slots = self.main_config['n_deck_slots']

        # Define the ranges of each sub-space
        self.buy_actions = range(n_shop_slots * n_deck_slots)
        self.freeze_actions = range(self.buy_actions.stop,
                                    self.buy_actions.stop + n_deck_slots)
        self.reroll_action = self.freeze_actions.stop
        self.sell_actions = range(self.reroll_action + 1,
                                  self.reroll_action + 1 + n_deck_slots)
        self.reorder_actions = range(self.sell_actions.stop,
                                     self.sell_actions.stop +
                                     np.power(n_deck_slots, 2, dtype=int))
        self.end_turn_action = self.reorder_actions.stop

        # Define the entire action space
        self.action_space = spaces.Discrete(self.end_turn_action+1)

        """
        Observations can be conceptualized as multiple observation spaces:
            (1) Number of trophies: Discrete N_TROPHIES
            (2) Number of hearts: Discrete N_HEARTS
            (3) Amount of gold: Discrete MAX_GOLD_VALUE      
            (4) Game rounds passed: Discrete MAX_INTEGER
            (5) Deck: Dict
            (6) Shop: Dict   

        The keys of the deck dictionary will be the slot number. Corresponding
        to each slot are:
            - id: row index of this pet in config csv
            - gold: gold value of this pet
            - health: health points of this pet
            - attack: attack points of this pet
            - food_id: row index of this pet's attached food in config csv       

        The keys of the shop dictionary will be the slot number. Corresponding
        to each slot are:
            - type: 0 if food, 1 if pet
            - id: row index of this food or pet in config csv
            - gold: gold value of this food or pet
            - health: health if pet, 0 if food
            - attack: attack if pet, 0 if food
            - food_id: some pets come with food already attached, Empty if food
        """
        max_pet_id = len(self.pets_config)
        max_food_id = len(self.food_config)
        max_gold_value = max(
            max(self.pets_config['Gold']),
            max(self.food_config['Gold'])
        )
        max_health = self.main_config['max_health']
        max_attack = self.main_config['max_attack']
        n_max_tokens = self.main_config['n_max_tokens']
        max_level = self.main_config['max_level']

        # Define the deck subspace
        self.deck_space = spaces.Dict(dict([
            (i, spaces.Dict({
                'id': spaces.Discrete(max_pet_id),
                'gold': spaces.Discrete(max_gold_value+1),
                'health': spaces.Discrete(max_health+1),
                'attack': spaces.Discrete(max_attack+1),
                'level': spaces.Discrete(max_level+1),
                'exp': spaces.Discrete(max_level+1),
                'tokens': spaces.MultiDiscrete([max_pet_id] * n_max_tokens),
                'food_id': spaces.Discrete(max_food_id)
            })) for i in range(n_deck_slots)
        ]))

        # Define the shop subspace
        self.IS_FOOD, self.IS_PET = 0, 1
        max_obj_id = max(max_pet_id, max_food_id)
        self.shop_space = spaces.Dict(dict([
            (i, spaces.Dict({
                'type': spaces.Discrete(2),
                'id': spaces.Discrete(max_obj_id),
                'gold': spaces.Discrete(max_gold_value+1),
                'health': spaces.Discrete(max_health+1),
                'attack': spaces.Discrete(max_attack+1),
                'food_id': spaces.Discrete(max_food_id)
            })) for i in range(n_shop_slots)
        ]))

        # Define the entire obsevation space
        self.observation_space = spaces.Dict({
            'n_trophies': spaces.Discrete(self.main_config['n_trophies']+1),
            'n_hearts': spaces.Discrete(self.main_config['n_hearts']+1),
            'n_gold': spaces.Discrete(np.iinfo(np.int32).max),
            'n_rounds': spaces.Discrete(np.iinfo(np.int32).max),
            'shop': self.shop_space,
            'deck': self.deck_space
        })

        # Initial game state
        self.reset()
        self.state = self._get_obs()

        # Other vars that aren't included in observations
        self.n_cans = 0

        # Check that the initial observation is valid
        try:
            assert self.observation_space.contains(self.state), \
                'Invalid initial state'
        except Exception as e:
            print(e)
            self.render(mode='ansi')
            exit()

    def step(self, action):
        # Check that action is valid
        assert self.action_space.contains(action), \
            f'Action {action} is invalid; action space range is {self.action_space}'

        # Process actions
        reward = 0
        observation = self._get_obs()
        if action in self.buy_actions:
            pass
        elif action in self.freeze_actions:
            pass
        elif action == self.reroll_action:
            pass
        elif action in self.sell_actions:
            pass
        elif action in self.reorder_actions:
            pass
        elif action == self.end_turn_action:
            pass

        # Get new observation and check for end-of-game
        observation = self._get_obs()
        lost = observation['n_hearts'] == 0
        won = observation['n_trophies'] == self.main_config['n_trophies']
        done = lost or won

        # Diagnostic information
        info = {'game_result': 'won' if won else 'lost'}

        return observation, reward, done, info

    def reset(self):
        # Initialize the shop with non-empty slots
        shop = {}
        max_pet_id = len(self.pets_config)
        max_food_id = len(self.food_config)
        n_pets, n_food = self.main_config['n_shop_slots'].values()
        rng = np.random.default_rng()

        # Add pets
        for i in range(n_pets):
            id = rng.choice(max_pet_id, p=self.pets_config['Roll_chance'])
            pet = self.pets_config.loc[id]
            shop[i] = {
                'type': self.IS_PET,
                'id': id,
                'gold': pet['Gold'],
                'health': pet['Health'],
                'attack': pet['Attack'],
                'food_id': pet['Food_id']
            }

        # Add food
        for i in range(n_food):
            id = rng.choice(max_food_id, p=self.food_config['Roll_chance'])
            food = self.food_config.loc[id]
            shop[i+n_pets] = {
                'type': self.IS_FOOD,
                'id': id,
                'gold': food['Gold'],
                'health': 0,
                'attack': 0,
                'food_id': self.EMPTY_ID
            }

        # Initialize the deck with empty slots
        n_max_tokens = self.main_config['n_max_tokens']
        n_deck_slots = self.main_config['n_deck_slots']
        deck = dict([
            (i, {
                'id': self.EMPTY_ID,
                'gold': 0,
                'health': 0,
                'attack': 0,
                'level': 1,
                'exp': 0,
                'tokens': [self.EMPTY_ID] * n_max_tokens,
                'food_id': self.EMPTY_ID
            }) for i in range(n_deck_slots)
        ])

        # Set state
        self.state = {
            'n_trophies': 0,
            'n_hearts': self.main_config['n_hearts'],
            'n_gold': self.main_config['n_gold'],
            'n_rounds': 0,
            'shop': shop,
            'deck': deck
        }

    def _get_obs(self):
        return self.state

    def render(self, mode='ansi'):
        if mode == 'ansi':
            def print_table(title, table):
                table_width = len(table.split('\n')[1])
                border = '=' * table_width
                title_width = len(title)
                pad_width = (table_width - title_width) // 2 - 1
                padding = ' ' * pad_width
                print()
                print(border)
                print(padding, title.upper())
                print(border)
                print(table)

            # Get the raw game state
            state = self._get_obs()

            # Print main game vars
            main_game_vars = ['n_trophies', 'n_hearts',
                              'n_gold', 'n_rounds']
            table = [[state[k] for k in main_game_vars]]
            fmt_table = tabulate(table, headers=main_game_vars)
            print_table('game attributes', fmt_table)

            # Print deck
            n_deck_slots = self.main_config['n_deck_slots']
            n_max_tokens = self.main_config['n_max_tokens']
            table = []
            for i in range(n_deck_slots):
                # Change ID to human-readable name
                id = state['deck'][i]['id']
                state['deck'][i]['id'] = self.pets_config.loc[id]['Name']
                # Change token IDs to human-readable names
                for j in range(n_max_tokens):
                    id = state['deck'][i]['tokens'][j]
                    state['deck'][i]['tokens'][j] = self.pets_config.loc[id]['Name']
                # Change food ID to human-readable name
                food_id = state['deck'][i]['food_id']
                state['deck'][i]['food_id'] = self.food_config.loc[food_id]['Name']
                # Append this slot to the table
                table.append(state['deck'][i])
            fmt_table = tabulate(table, headers='keys')
            print_table('deck', fmt_table)

            # Print shop
            n_pets, n_food = self.main_config['n_shop_slots'].values()
            table = []
            for i in range(n_pets):
                # Change ID to human-readable name
                id = state['shop'][i]['id']
                state['shop'][i]['id'] = self.pets_config.loc[id]['Name']
                # Change type to "pet"
                state['shop'][i]['type'] = 'pet'
                # Append this slot to the table
                table.append(state['shop'][i])
            for i in range(n_food):
                # Offset by pets
                j = i + n_pets
                # Change ID to human-readable name
                id = state['shop'][j]['id']
                state['shop'][j]['id'] = self.food_config.loc[id]['Name']
                # Change type to "food"
                state['shop'][j]['type'] = 'food'
                # Append this slot to the table
                table.append(state['shop'][j])
            fmt_table = tabulate(table, headers='keys')
            print_table('shop', fmt_table)

        else:
            super(GameEnv, self).render(mode=mode)

    def close(self):
        pass
