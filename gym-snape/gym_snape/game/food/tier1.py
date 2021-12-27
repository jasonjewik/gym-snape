from gym_snape.game.food.food import Food


class Apple(Food):
    def __init__(self):
        self._name = 'APPLE'

    def on_use(self, index):
        """Give a deck pet +1 attack, +1 health."""
        if self._deck[index]:
            self._deck[index].attack += 1
            self._deck[index].health += 1


class Honey(Food):
    def __init__(self):
        self._name = 'HONEY'

    def on_use(self, index):
        """Give a deck pet the Honey Bee effect."""
        if self._deck[index]:
            self._deck[index].effect = 'Bee'


ROLL_CHANCES = {
    Apple: 1/2,
    Honey: 1/2
}
