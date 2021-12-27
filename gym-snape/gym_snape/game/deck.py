from gym_snape.game.pets.pet import Pet
from gym_snape.game.food.food import Food


class Deck:
    def __init__(self):
        self.SIZE = 5
        self._pets = [None] * self.SIZE
        self._last_op_success = True

    def __getitem__(self, index):
        return self._pets[index]

    def __setitem__(self, index, value):
        self._last_op_success = True
        if value is None:
            self._pets[index] = None
        elif isinstance(value, Pet):
            if self._pets[index] is None:
                value.assign_friends(self)
                self._pets[index] = value
                for pet in self:
                    if pet:
                        pet.on_friend_summoned(index)
            elif type(self[index]) == type(value) and self[index].can_level():
                self._pets[index] += value
            else:
                self._last_op_success = False
        elif isinstance(value, Food):
            if self._pets[index]:
                value.assign_deck(self)
                value.on_use(index)
                self._pets[index].on_consume_food()
            else:
                self._last_op_success = False
        else:
            self._last_op_success = False

    def __delitem__(self, index):
        self._pets[index] = None

    def __len__(self):
        return self.SIZE

    def __str__(self):
        substrs = []
        for i in range(len(self._pets)-1, -1, -1):
            pet = self._pets[i]
            if pet:
                pet_str_arr = str(pet).replace('+', str(i)).split('\n')
                pet_str_arr = [p + '\n' for p in pet_str_arr]
                substrs.append(pet_str_arr)
            else:
                border = f'{i}----------{i}\n'
                rows = ['|          |\n'] * 6
                substrs.append([border] + rows + [border])
        result = ''
        for _ in range(8):
            for i in range(len(substrs)):
                if i == len(substrs) - 1:
                    result += substrs[i].pop(0)
                else:
                    result += substrs[i].pop(0).strip()
        result = result.strip()
        return result

    def is_empty(self):
        count = sum([1 for p in self if p])
        return count == 0

    @property
    def last_op_success(self):
        return self._last_op_success

    @property
    def success(self):
        return self.last_op_success

    def swap(self, source, destination):
        src_pet, self[source] = self[source], None
        dest_pet, self[destination] = self[destination], None
        self[source], self[destination] = dest_pet, src_pet
        self._last_op_success = True

    def merge(self, source, destination):
        self[destination] = self[source]
        if self.success:
            del self[source]

    def shift_forward(self):
        i = 0
        while i < self.SIZE and self._pets[0] is None:
            self._pets = self._pets[1:] + [None]
            i += 1
