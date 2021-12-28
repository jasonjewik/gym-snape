# Standard library imports
from typing import Literal, Final

# Local application imports
from gym_snape.game.food import Food
from gym_snape.game.pets import Pet


class Deck:
    """
    The deck used in the game.
    """

    def __init__(self):
        self.N_DECK_SLOTS: Final = 5
        self._pets = [None] * self.N_DECK_SLOTS
        self._last_op_success = True

    def __getitem__(self, index: int) -> Pet:
        return self._pets[index]

    def __setitem__(self, index: int, value: Pet | Food | None):
        self._last_op_success = True

        # Clear the selected slot (equivalent to del)
        if value is None:
            self._pets[index] = None

        # Put a pet into the selected slot
        elif isinstance(value, Pet):
            # Insert pet into empty slot
            if self._pets[index] is None:
                value.assign_friends(self)
                self._pets[index] = value
                for pet in self:
                    if pet:
                        pet.on_friend_summoned(index)
            # Add pet to slot containing pet of same type
            elif type(self[index]) == type(value) and self[index].can_level():
                self._pets[index] += value
            # Any other operation is a no-op
            else:
                self._last_op_success = False

        # Put a food item into the selected slot
        elif isinstance(value, Food):
            value.assign_deck(self)
            value.on_use(index)
            # If food was successfully consumed and the slot contains a pet
            if value.success and self._pets[index]:
                self._pets[index].on_consume_food()
            self._last_op_success = value.success

        # Any other argument is invalid
        else:
            raise TypeError('value must be Pet, Food, or None')

    def __delitem__(self, index: int):
        """Sets the deck slot at the given index to None."""
        self._pets[index] = None

    def __len__(self) -> Literal[5]:
        """The default number of deck slots is 5."""
        return self.N_DECK_SLOTS

    def __str__(self):
        """
        Returns the state of the deck as a set of cards.
        """
        # Get the string representation of each indvidual slot
        substrs = []

        # Iterate through the deck backwards to match the deck layout in the
        # original Super Auto Pets
        for i in range(len(self._pets)-1, -1, -1):
            pet = self._pets[i]
            if pet:  # representation for a filled slot
                # Put the index of the deck slot in the corner of the card
                pet_str_arr = str(pet).replace('+', str(i)).split('\n')
                pet_str_arr = [p + '\n' for p in pet_str_arr]
                substrs.append(pet_str_arr)
            else:  # representation for the empty slot
                border = f'{i}----------{i}\n'
                rows = ['|          |\n'] * 6
                substrs.append([border] + rows + [border])

        # Put the cards together by attaching the ends
        result = ''
        for _ in range(len(substrs[0])):
            for i in range(len(substrs)):
                if i == len(substrs) - 1:
                    result += substrs[i].pop(0)
                else:
                    result += substrs[i].pop(0).strip()
        result = result.strip()
        return result

    @property
    def success(self):
        return self._last_op_success

    def is_empty(self):
        """Returns True if all slots are empty, False otherwise."""
        count = sum([1 for p in self if p])
        return count == 0

    def swap(self, source: int, destination: int):
        """
        Swaps the contents of two deck slots.

        Explicitly does NOT perform a merge, even if the pets contained in the
        two specified slots are of the same type.

        Parameters
        ----------
        source: int
            The source deck slot.

        destination: int
            The destination deck slot.

        Examples
        ----------
        See the docstring for `game.Game.swap`.
        """
        try:
            src_pet, self[source] = self[source], None
            dest_pet, self[destination] = self[destination], None
            self[source], self[destination] = dest_pet, src_pet
            self._last_op_success = True
        except:
            self._last_op_success = False

    def merge(self, source: int, destination: int):
        """
        Merges the contents of two deck slots.

        If the pets contained in the two specified deck slots cannot be merged,
        this is a no-op.

        Parameters
        ----------
        source: int
            The source deck slot.

        destination: int
            The destination deck slot (where the merged pet will be).

        Examples
        ----------
        See the docstring for `game.Game.merge`.
        """
        self[destination] = self[source]
        if self.success:
            del self[source]

    def shift_forward(self):
        """
        Shifts the deck forward until the 0th slot is non-empty.

        In the case that the entire deck is empty, this is basically a no-op.
        """
        i = 0
        while i < self.N_DECK_SLOTS and self._pets[0] is None:
            self._pets = self._pets[1:] + [None]
            i += 1
