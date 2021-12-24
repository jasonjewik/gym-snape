from gym_snape.game.food.food import Food


class Apple(Food):
    def on_use(self, index):
        """Give a deck pet +1 attack, +1 health."""
        if self._deck[index]:
            self._deck[index].attack += 1
            self._deck[index].health += 1


class Honey(Food):
    def on_use(self, index):
        """Give a deck pet a Honey Bee."""
        if self._deck[index]:
            pass
