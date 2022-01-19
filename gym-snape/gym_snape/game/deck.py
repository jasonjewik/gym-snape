# Standard library imports
from copy import deepcopy
from typing import Final, Literal, Optional

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
        self._game = None

    def __getitem__(self, index: int) -> Optional[Pet]:
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
                for pet in self:  # trigger on summon abilities
                    if pet and id(pet) != id(value):
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
                self._pets[index].on_eat_food()
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

    def index(self, pet: Pet):
        """Returns the index of the given pet, -1 if not found."""
        self._last_op_success = False
        index = -1
        for i in range(len(self)):
            if self[i] and id(self[i]) == id(pet):
                index = i
                self._last_op_success = True
        return index

    def append(self, pet: Pet):
        """Puts the given pet into the first available slot from the back."""
        self._last_op_success = False
        for i in range(len(self) - 1, -1, -1):
            if self[i] is None:
                self[i] = pet
                self._last_op_success = True
                break

    def insert(self, index: int, pet: Pet):
        """
        Puts the given pet into the given deck slot.

        If the slot is filled, we try to create room by shifting either forward
        or backward.

        Parameters
        ----------
        index: int
            The deck slot to insert into.

        pet: Pet
            The pet to insert.
        """
        self._last_op_success = False
        if self[index] is None:
            self[index] = pet
            self._last_op_success = True
        else:
            # Try shifting backward
            self._shift_backward(index)
            if self[index] is None:
                self[index] = pet
                self._last_op_success = True
            # Try shifting forward
            if not self.success:
                self._shift_forward(index)
                if self[index] is None:
                    self[index] = pet
                    self._last_op_success = True

    def assign_game(self, value):
        """
        Assigns a game instance to this deck.
        """
        self._game = value

    def prep_for_battle(self):
        """
        Prepares this deck for usage in combat.

        Creates and saves copies of all the current deck pets, to be restored
        after the battle by `battle_cleanup`.

        Notes
        ----------
        We cannot simply use Python's copy.deepcopy on an instance of the deck
        to prepare it for battle because copy.deepcopy will assign to each deck
        pet a new instance of Game to its _game variable. Therefore, when deck
        deck pets hand up their ability casts to the battle manager, they will 
        be giving it to the copy of the Game rather than the original Game 
        instance which is actually running the battle. 

        Raises
        ----------
        RuntimeError if `prep_for_battle` was called previously and not
        followed up with `battle_cleanup` (i.e., it is illegal to call this
        method consecutively with cleaning up in between each call)

        See also
        ----------
        - `battle_cleanup`
        """
        # Check if called previously without cleanup
        try:
            self.__prebattle_deck_copy
            raise RuntimeError(
                'prep_for_battle was called previously without cleanup')
        except AttributeError:
            pass

        # We use a deepcopy here since it will ensure that the hp, attack, and
        # other stats of the saved copy are not modified by the battle
        self.__prebattle_deck_copy = deepcopy(self._pets)

    def battle_cleanup(self):
        """
        Cleans up any changes made during the battle.

        Restores all pets to their state as they were before the battle.

        Raises
        ----------
        RuntimeError if `prep_for_battle` is not called first.

        See also
        ----------
        - `prep_for_battle`
        """
        try:  # check if prep_for_battle was called first
            self.__prebattle_deck_copy
        except AttributeError:
            raise RuntimeError('prep_for_battle has not yet been called')

        # Restore attributes of each pet
        for i in range(len(self._pets)):
            self._pets[i] = self.__prebattle_deck_copy[i]
            if self._pets[i]:
                self._pets[i].assign_game(self._game)
                self._pets[i].assign_friends(self._game.deck)
                self._pets[i].assign_shop(self._game.shop)

        # Remove temporary variable to indicate cleanup complete
        del self.__prebattle_deck_copy

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

    def shift_all_forward(self):
        """
        Shifts the deck forward until the 0th slot is non-empty.

        In the case that the entire deck is empty, this is basically a no-op.
        """
        i = 0
        while i < self.N_DECK_SLOTS and self._pets[0] is None:
            self._pets = self._pets[1:] + [None]
            i += 1

    def _shift_forward(self, index: int):
        """
        Shifts all slots starting with the given index forward.

        Tries to make the given slot empty.
        """
        front = self._pets[:index+1]
        back = self._pets[index+1:]
        i = len(front) - 1
        while i > -1:  # this means we tried pushing everything already
            if front[-1] is None:  # we have cleared a spot
                break
            elif front[i] is None:  # we have space to push up
                front = front[:i] + front[i+1:] + [None]
            else:
                i -= 1
        self._pets = front + back

    def _shift_backward(self, index: int):
        """
        Shifts all slots starting with the given index backward.

        Tries to make the given slot empty.
        """
        front = self._pets[:index]
        back = self._pets[index:]
        i = 0
        while i < len(back):  # this means we tried pushing everything already
            if back[0] is None:  # we have cleared a spot
                break
            elif back[i] is None:  # we have space to push back
                back = [None] + back[:i] + back[i+1:]
            else:
                i += 1
        self._pets = front + back
