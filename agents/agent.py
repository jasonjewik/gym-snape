# Standard library imports
from abc import ABC, abstractmethod

# Local application imports
from gym_snape import Snape


class Agent(ABC):
    """Base class for all agents."""

    def __init__(self, env: Snape, *args, **kwargs):
        self._env = env

    @abstractmethod
    def select_action(self, *args, **kwargs) -> int:
        """How the agent makes a decision."""
        raise NotImplementedError
