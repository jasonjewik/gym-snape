# Local application imports
from .agent import Agent
from gym_snape import Snape


class RandomAgent(Agent):
    def __init__(self, env: Snape):
        super().__init__(env)

    def select_action(self) -> int:
        action = self._env.action_space.sample()
        return action
