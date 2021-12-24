from abc import ABC, abstractmethod


class Food(ABC):
    @abstractmethod
    def on_use(self, index):
        """What happens when the food is used."""
        raise NotImplementedError

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, value):
        self._deck = value

    @property
    def shop(self):
        return self._shop

    @shop.setter
    def shop(self, value):
        self._shop = value
