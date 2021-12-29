# Local application imports
from .agent import Agent
from gym_snape import Snape

# Third party imports
import numpy as np


class RuleBasedController(Agent):
    def __init__(self, env: Snape):
        super().__init__(env)
        self._prev_deck = None
        self._prev_shop = None

    def select_action(self, obs) -> int:
        """
        Selects an action based on the given observation.
        """
        action = -1

        # If out of gold, begin battle
        if obs['n_gold'] == 0:
            action = self._env.end_turn_action

        # If less than 3 gold, randomly decide to freeze or roll shop
        elif obs['n_gold'] < 3:
            if np.random.randint(2) == 0:  # roll shop
                action = self._env.roll_action
            else:  # freeze random shop slot, might try freezing an empty slot!
                index = np.random.randint(len(obs['shop'].keys()))
                action = self._env.freeze_actions.start + index

        # If can buy something (>=3 gold) and current turn number is less than
        # 9 and we have room in the deck, buy pet with highest health
        elif obs['n_gold'] >= 3 and obs['n_turns'] < 9:
            deck_index = -1
            for i in obs['deck']:
                slot = obs['deck'][i]
                if slot['type'] == self._env.IS_EMPTY:
                    deck_index = i
                    break
            if deck_index != -1:  # we found an empty slot
                # In this case, look for the highest health pet
                highest_health, shop_index = 0, -1
                for i in obs['shop']:
                    slot = obs['shop'][i]
                    if (slot['type'] == self._env.IS_PET and
                            slot['health'] > highest_health):
                        highest_health = slot['health']
                        shop_index = i
                if shop_index != -1:  # a pet was found
                    # To buy from shop_index and place into deck_index, use
                    # this formula:
                    n_deck_slots = len(self._env.game.deck)
                    action = shop_index * n_deck_slots + deck_index
                    action += self._env.buy_actions.start
                else:   # do nothing - later we take a random action
                    pass
            else:  # we could not find an empty slot
                # In this case, sell a random deck animal
                choices = []
                for i in obs['deck']:
                    slot = obs['deck'][i]
                    if slot['type'] == self._env.IS_PET:
                        choices.append(i)
                deck_index = np.random.choice(choices, size=1)[0]
                action = self._env.sell_actions.start + deck_index

        # Action was not explicitly selected or deck/shop did not change
        same_deck = self._prev_deck is not None and self._prev_deck == obs['deck']
        same_shop = self._prev_shop is not None and self._prev_shop == obs['shop']
        if action == -1 or same_deck or same_shop:
            action = self._env.action_space.sample()  # take a random action

        # Track previous observation deck/space
        self._prev_deck = obs['deck']
        self._prev_shop = obs['shop']

        return action
