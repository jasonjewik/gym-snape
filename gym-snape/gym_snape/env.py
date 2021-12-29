# Standard library imports
from pprint import pprint

# Local application imports
from gym_snape.game import Game
from gym_snape.game.pets import Pet
from gym_snape.game.food import Food

# Third-party imports
import gym
from gym import spaces
import numpy as np


class Snape(gym.Env):
    metadata = {'render.modes': ['ansi']}   

    def __init__(self, display: bool = False):
        super().__init__()

        # Create a game instance
        self.game = Game(display=display)

        # Initial opponent is no one
        self._opponent = None

        """
        N = total number of shop slots (empty and non-empty)
        M = total number of deck slots (empty and non-empty)

        From the human POV, game controls can be conceptualized as discrete
        action spaces:
            (1) Roll shop: Discrete 2
                - Pressed + no-op
            (2) Freeze shop slot: Discrete N+1
                - N slots + no-op
            (3) Buy from shop: Discrete (N*M)+1
                - N*M pairs of shop slots and deck slots + no-op
            (4) Sell from deck: Discrete M+1
                - M deck slots + no-op
            (5) Swap two deck slots: Discrete (M*M)+1
                - M*M pairs of source/destination deck slots + no-op
            (6) Merge two deck slots: Discrete (M*M)+1
                - M*M pairs of source/destination deck slots + no-op
            (7) End turn (begin combat): Discrete 2
                - Pressed + no-op

        Since we want an agent to take exactly one action at a time, we can
        combine all these sub-spaces into one large discrete action space. This
        also removes the need for no-op actions.

        So the entire action space will be:
        Discrete (1)+(N)+(N*M)+(M)+(M*M)+(M*M)+(1)
        """

        # Determine N and M
        self._n_shop_slots = len(self.game.shop)
        self._n_deck_slots = len(self.game.deck)

        # Define the ranges of each sub-space
        self.roll_action = 0
        self.freeze_actions = range(1, 1+self._n_shop_slots)
        self.buy_actions = range(
            self.freeze_actions.stop,
            self.freeze_actions.stop + self._n_shop_slots * self._n_deck_slots
        )
        self.sell_actions = range(
            self.buy_actions.stop,
            self.buy_actions.stop + self._n_deck_slots
        )
        self.swap_actions = range(
            self.sell_actions.stop,
            self.sell_actions.stop + self._n_deck_slots * self._n_deck_slots
        )
        self.merge_actions = range(
            self.swap_actions.stop,
            self.swap_actions.stop + self._n_deck_slots * self._n_deck_slots
        )
        self.end_turn_action = self.merge_actions.stop

        # Define the entire action space
        self.action_space = spaces.Discrete(self.end_turn_action+1)

        """
        Observations can be conceptualized as multiple observation spaces:
            (1) Game turn number: Discrete MAX_INTEGER
            (2) Number of lives: Discrete N_LIVES
            (3) Number of trophies: Discrete N_TROPHIES
            (4) Amount of gold: Discrete MAX_GOLD_VALUE      
            (5) Actions taken: Discrete MAX_INTEGER
            (5) Deck: Dict
            (6) Shop: Dict   

        The keys of the deck dictionary will be the slot number. Corresponding
        to each slot are:
            - type: 0 if empty, 1 if pet
            - id: id number of this pet type
            - health: health points of this pet
            - health_buff: (temp) health buff points on this pet
            - attack: attack points of this pet
            - attack_buff: (temp) attack buff points on this pet
            - effect_id: id of effect type applied to this pet
            - experience: experience points
            - level: current level of this pet
            - gold_cost: resale value of this pet

        The keys of the shop dictionary will be the slot number. Corresponding
        to each slot are:
            - type: 0 if empty, 1 if pet, 2 if food
            - id: id of this item
            - health: health if pet, 0 if food
            - health_buff: (temp) health buff if pet, 0 if food
            - attack: attack if pet, 0 if food
            - attack_buff: (temp) attack buff if pet, 0 if food
            - effect_id: effect if pet, -1 if food
            - gold_cost: purchase price of this item
            - is_frozen: 0 if false, 1 if true
        """
        # The following values are taken from the game's default configuration
        INT_MAX = np.iinfo(np.int32).max
        max_gold_value = 3
        max_health = 50
        max_attack = 50
        max_experience = 3
        max_level = 3

        # Constants for slot type
        self.IS_EMPTY = 0
        self.IS_PET = 1
        self.IS_FOOD = 2

        # Constants for frozen/unfrozen
        self.IS_FROZEN = 0
        self.NOT_FROZEN = 1

        # Define the deck subspace
        self.deck_space = spaces.Dict(dict([
            (i, spaces.Dict({
                'type': spaces.Discrete(2),
                'id': spaces.Discrete(INT_MAX),
                'health': spaces.Discrete(max_health+1),
                'health_buff': spaces.Discrete(max_health+1),
                'attack': spaces.Discrete(max_attack+1),
                'attack_buff': spaces.Discrete(max_attack+1),
                'effect_id': spaces.Discrete(INT_MAX),
                'experience': spaces.Discrete(max_experience+1),
                'level': spaces.Discrete(max_level+1),
                'gold_cost': spaces.Discrete(max_gold_value+1)
            })) for i in range(self._n_deck_slots)
        ]))

        # Define the shop subspace
        self.shop_space = spaces.Dict(dict([
            (i, spaces.Dict({
                'type': spaces.Discrete(3),
                'id': spaces.Discrete(INT_MAX),
                'health': spaces.Discrete(max_health+1),
                'health_buff': spaces.Discrete(max_health+1),
                'attack': spaces.Discrete(max_attack+1),
                'attack_buff': spaces.Discrete(max_attack+1),
                'effect_id': spaces.Discrete(INT_MAX),
                'gold_cost': spaces.Discrete(max_gold_value+1),
                'is_frozen': spaces.Discrete(2),
            })) for i in range(self._n_shop_slots)
        ]))

        # The following values are taken from the game's default configuration
        n_max_lives = 10
        n_max_trophies = 10
        gold_per_turn = 10

        # Define the entire obsevation space
        self.observation_space = spaces.Dict({
            'n_turns': spaces.Discrete(INT_MAX),
            'n_lives': spaces.Discrete(n_max_lives+1),
            'n_trophies': spaces.Discrete(n_max_trophies+1),
            'n_gold': spaces.Discrete(gold_per_turn+1),
            'n_actions': spaces.Discrete(INT_MAX),
            'deck': self.deck_space,
            'shop': self.shop_space
        })

        # Initial game state
        self.state = self._get_obs()

        # Check that the initial observation is valid
        if not self.observation_space.contains(self.state):
            print('Invalid initial state')
            pprint(self.state)

    def assign_opponent(self, opponent):
        """Assign an opponent (environment object) to this environment."""
        self._opponent = opponent

    def step(self, action):
        # Check that action is valid
        assert self.action_space.contains(action), \
            f'Action {action} is invalid; action space range is {self.action_space}'

        # Process actions
        if action == self.roll_action:
            self.game.roll()
        elif action in self.freeze_actions:
            index = action - self.freeze_actions.start
            self.game.freeze(index)
        elif action in self.buy_actions:
            a = action - self.buy_actions.start
            indices = divmod(a, self._n_deck_slots)
            self.game.buy(indices)
        elif action in self.sell_actions:
            index = action - self.sell_actions.start
            self.game.sell(index)
        elif action in self.swap_actions:
            a = action - self.swap_actions.start
            indices = divmod(a, self._n_deck_slots)
            self.game.swap(indices)
        elif action in self.merge_actions:
            a = action - self.merge_actions.start
            indices = divmod(a, self._n_deck_slots)
            self.game.merge(indices)
        elif action == self.end_turn_action:
            if self._opponent:
                self.game.challenge(self._opponent.game)
            else:
                raise AttributeError('opponent has not yet been assigned')

        # Get new observation and check for end-of-game
        observation = self._get_obs()
        done = self.game.game_over

        # Small negative reward for each action taken
        reward = -1

        # Extra reward for game won or lost
        if self.game.won:
            reward = 100
        elif self.game.lost:
            reward = -100

        # Diagnostic information
        info = {}

        return observation, reward, done, info

    def reset(self):
        self.game = Game()  # create a new game

    def _get_obs(self):
        # Get deck state
        deck_state = {}
        for i, pet in enumerate(self.game.deck):
            if pet:
                deck_state[i] = {
                    'type': self.IS_PET,
                    'id': pet.id,
                    'health': pet.health,
                    'health_buff': pet.health_buff,
                    'attack': pet.attack,
                    'attack_buff': pet.attack_buff,
                    'effect_id': pet.effect_id,
                    'experience': pet.experience,
                    'level': pet.level,
                    'gold_cost': pet.gold_cost,
                }
            else:
                deck_state[i] = {
                    'type': self.IS_EMPTY,
                    'id': 0,
                    'health': 0,
                    'health_buff': 0,
                    'attack': 0,
                    'attack_buff': 0,
                    'effect_id': 0,
                    'experience': 0,
                    'level': 0,
                    'gold_cost': 0
                }

        # Get shop state
        shop_state = {}
        for i, slot in enumerate(self.game.shop):
            if isinstance(slot.item, Pet):
                pet = slot.item
                shop_state[i] = {
                    'type': self.IS_PET,
                    'id': pet.id,
                    'health': pet.health,
                    'health_buff': pet.health_buff,
                    'attack': pet.attack,
                    'attack_buff': pet.attack_buff,
                    'effect_id': pet.effect_id,
                    'gold_cost': pet.gold_cost,
                    'is_frozen': int(slot.is_frozen)
                }
            elif isinstance(slot.item, Food):
                food = slot.item
                shop_state[i] = {
                    'type': self.IS_FOOD,
                    'id': food.id,
                    'health': food.health,
                    'health_buff': 0,
                    'attack': food.attack,
                    'attack_buff': 0,
                    'effect_id': 0,
                    'gold_cost': food.gold_cost,
                    'is_frozen': int(slot.is_frozen)
                }
            else:
                shop_state[i] = {
                    'type': self.IS_EMPTY,
                    'id': 0,
                    'health': 0,
                    'health_buff': 0,
                    'attack': 0,
                    'attack_buff': 0,
                    'effect_id': 0,
                    'gold_cost': 0,
                    'is_frozen': int(slot.is_frozen)
                }

        # Return observation
        observation = {
            'n_turns': self.game.turn,
            'n_lives': self.game.lives,
            'n_trophies': self.game.trophies,
            'n_gold': self.game.gold,
            'n_actions': self.game.actions_taken,
            'deck': deck_state,
            'shop': shop_state
        }
        return observation

    def render(self, mode='ansi'):
        if mode == 'ansi':
            print(str(self.game))
        else:
            super().render(mode=mode)

    def close(self):
        pass
