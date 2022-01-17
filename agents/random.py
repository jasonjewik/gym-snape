# Local application imports
from .agent import Agent
from gym_snape import Snape


class Random(Agent):
    def __init__(self, env: Snape):
        super().__init__(env)

    def select_action(self, obs) -> int:
        """
        Selects an action based on the given observation.
        """
        action = self._env.action_space.sample()  # take a random action
        return action
