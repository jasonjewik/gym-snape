from abc import ABC, abstractmethod


class Food(ABC):
    @abstractmethod
    def on_use(self, index):
        """What happens when the food is used."""
        raise NotImplementedError

    def __str__(self):
        width = 10
        border = '+----------+'
        name_row = f'|{self._name:{width}}|'
        empty_row = ['|          |'] * 5
        result = [border, name_row] + empty_row + [border]
        result = '\n'.join(result)
        return result

    def assign_deck(self, value):
        self._deck = value

    def assign_shop(self, value):
        self._shop = value
