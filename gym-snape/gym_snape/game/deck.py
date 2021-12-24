from gym_snape.game.pets.pet import Pet


class Deck:
    def __init__(self):
        self.SIZE = 5
        self._pets = [None] * self.SIZE

    def __getitem__(self, index):
        return self._pets[index]

    def __setitem__(self, index, value):
        if value is None:
            self._pets[index] = None
        elif isinstance(value, Pet):
            if self._pets[index] is None:
                value.assign_deck(self)
                self._pets[index] = value
            elif type(self[index]) == type(value) and self[index].can_level():
                self._pets[index].experience += value.experience + 1
        # elif isinstance(value, Food):
        #   pass

    def __delitem__(self, index):
        self._pets[index] = None

    def __len__(self):
        return self.SIZE

    def __str__(self):
        return ' '.join([str(x) for x in self])

    def swap(self, source, destination):
        src_pet, self[source] = self[source], None
        dest_pet, self[destination] = self[destination], None
        self[source], self[destination] = dest_pet, src_pet
