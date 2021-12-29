# Standard library imports
from copy import deepcopy
from functools import wraps
from typing import Callable, final, Final, Optional, ParamSpec, TypeVar

# Local application imports
from gym_snape.game.effects import effects

# Typing definitions
P = ParamSpec('P')
T = TypeVar('T')


def capture_action(bound_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Pet`'s methods that captures actions when in battle so
    that the battle manager can control ability cast order."""
    @wraps(bound_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        if self.in_battle:  # append an entry to the game's ability log
            self._game.add_ability_to_cast((self, bound_method, args, kwargs))
        else:  # call the method immediately
            bound_method(self, *args, **kwargs)
    return _impl


def duplicate_action(bound_method: Callable[P, T]) -> Callable[P, T]:
    """A decorator for `Pet`'s methods that causes it to perform its action
    twice if in battle - basically for use by the Tiger."""
    @wraps(bound_method)
    def _impl(self, *args: P.args, **kwargs: P.kwargs) -> T:
        bound_method(self, *args, **kwargs)  # cast ability normally
        if self.in_battle and self._duplicate_as > 0:  # temporarily boost level
            prev_level = self._level
            self._level = self._duplicate_as
            bound_method(self, *args, **kwargs)  # cast ability again
            self._level = prev_level
    return _impl


class Pet:
    """
    The base class for pets.

    A pet's name must be at least 3 characters long and these first 3
    characters must be unique among all pets.
    """

    def __init__(self):
        self._MAX_ATTACK: Final = 50
        self._MAX_HEALTH: Final = 50
        self._EXP_TO_LEVEL_UP: Final = (2, 3)
        self._MAX_LEVEL: Final = len(self._EXP_TO_LEVEL_UP) + 1

        self._name = ''

        self._health = 0
        self._health_buff = 0

        self._attack = 0
        self._attack_buff = 0

        self._level = 1
        self.experience = 0

        self._gold_cost = 3
        self.effect = None

        self._in_battle = False
        self._duplicate_as = 0

    def __str__(self):
        """Returns a summary of the pet as a card."""
        width = 10

        # Indicate a health/attack buff with parentheses
        health_str = str(self.health+self.health_buff)
        attack_str = str(self.attack+self.attack_buff)
        if self.health_buff != 0:
            health_str = f'({health_str})'
        if self.attack_buff != 0:
            attack_str = f'({attack_str})'

        # Indicate no active effect with ellipsis
        if self.effect is None:
            effect = '...'
        else:
            effect = self.effect

        # Display the current experience over the experience needed to level up
        exp_as_frac = f'{self.experience}/{self._EXP_TO_LEVEL_UP[self.level-1]}'

        # Construct the card
        result = (
            '+----------+\n'
            f'|{self._name[:width]:{width}}|\n'
            f'|hp:  {health_str:{width-5}}|\n'
            f'|atk: {attack_str:{width-5}}|\n'
            f'|fct: {effect:<{width-5}}|\n'
            f'|exp: {exp_as_frac:{width-5}}|\n'
            f'|lvl: {self.level:<{width-5}}|\n'
            '+----------+'
        )
        return result

    def __add__(self, other):
        """
        Adding two pets of the same type will merge them.

        The merged pet has one more health than its healthiest component pet,
        up to the health cap. Likewise for its attack. The merged pet also
        receives all the health buffs and attack buffs of its components.

        Parameters
        ----------
        other: Pet
            The added pet must be of the same type as this pet.
        """
        if type(other) != type(self):
            raise TypeError(f'{other} is not of type {type(self)}')
        else:
            self.experience += other.experience + 1
            self.health = max(self.health, other.health) + 1
            self.attack = max(self.attack, other.attack) + 1
            self.health_buff = self.health_buff + other.health_buff
            self.attack_buff = self.attack_buff + other.attack_buff
        return self

    """
    The following comparators are for determining ability cast order in
    battle. See `gym_snape.game.Game.challenge`.
    """

    def __lt__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack < other.attack

    def __le__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack <= other.attack

    def __eq__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack == other.attack

    def __ne__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack != other.attack

    def __gt__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack > other.attack

    def __ge__(self, other):
        if not isinstance(other, Pet):
            raise TypeError(f'{type(other)} is not a subclass of Pet')
        else:
            return self.attack >= other.attack

    """End comparators."""

    @property
    def id(self) -> int:
        """
        Returns the concatenated integer representations of the first 3
        chars of the pet's name.
        """
        return int(''.join([str(ord(ch)) for ch in self._name[:3]]))

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        if type(value) == int:
            if self.effect == 'Glc':  # garlic armor damage modifier
                value = max(1, value-1)
            elif self.effect == 'Mln':  # melon armor damage modifier
                value = max(0, value-20)
                self.effect = None
            elif self.effect == 'Cct':  # coconut shield damage negation
                value = 0
                self.effect = None
            prev_health = self.health
            self._health = min(value, self._MAX_HEALTH)
            if self.health <= 0:
                self.on_faint()
            elif self.health < prev_health:
                self.on_hurt()
        else:
            raise TypeError('health must be an integer')

    @property
    def health_buff(self):
        return self._health_buff

    @health_buff.setter
    def health_buff(self, value: int):
        if type(value) == int:
            # Does not need a cap because health is capped
            self._health_buff = value
        else:
            raise TypeError('health buff must be an integer')

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value: int):
        if type(value) == int:
            self._attack = min(value, self._MAX_ATTACK)
        else:
            raise TypeError('attack must be an integer')

    @property
    def attack_buff(self):
        return self._attack_buff

    @attack_buff.setter
    def attack_buff(self, value: int):
        if type(value) == int:
            # Does not need a cap because attack is capped
            self._attack_buff = value
        else:
            raise TypeError('attack buff must be an integer')

    @property
    def level(self):
        return self._level

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if type(value) == int:
            self._experience = value
            while True:  # level as long as exp thresholds are crossed
                index = self.level - 1
                if index >= len(self._EXP_TO_LEVEL_UP):
                    break
                else:
                    exp_needed = self._EXP_TO_LEVEL_UP[self.level-1]
                    if self.experience >= exp_needed and self.can_level():
                        self._level += 1
                        self._experience -= exp_needed
                        self.on_level_up()
                    else:
                        break
            # At max level, experience is also maxed out
            if self.level == self._MAX_LEVEL:
                self._experience = self._EXP_TO_LEVEL_UP[-1]
        else:
            raise TypeError('argument must be castable to integer')

    @property
    def gold_cost(self):
        return self._gold_cost

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value: Optional[str]):
        if value is None or value in effects:
            self._effect = value
        else:
            raise ValueError(f'{value} not in {effects}')

    @property
    def effect_id(self) -> int:
        effect = '...' if self.effect is None else self.effect
        return int(''.join([str(ord(ch)) for ch in effect]))

    @property
    def in_battle(self) -> bool:
        return self._in_battle

    @in_battle.setter
    def in_battle(self, value: bool):
        if type(value) != bool:
            raise TypeError('in_battle must be a boolean')
        else:
            self._in_battle = value

    @property
    def duplicate_as(self) -> int:
        return self._duplicate_as

    @duplicate_as.setter
    def duplicate_as(self, value: int):
        if type(value) != int:
            raise TypeError('value must be an int')
        else:
            self._duplicate_as = value

    @final
    def assign_game(self, game):
        """Assigns a game to this pet."""
        self._game = game

    @final
    def assign_friends(self, deck):
        """Assigns a friendly deck to this pet."""
        self._friends = deck

    @final
    def assign_enemies(self, deck):
        """Assigns an enemy deck to this pet."""
        self._enemies = deck

    @final
    def assign_shop(self, shop):
        """Assigns a shop to this pet."""
        self._shop = shop

    @final
    def can_level(self) -> bool:
        """True if this pet's level is less than the max level."""
        return self.level < self._MAX_LEVEL

    @final
    def faint(self):
        """Forces this pet to faint."""
        self._health = 0
        self.on_faint()

    @final
    def zombify(self, health: int = 1, attack: int = 1):
        """
        Set the health/attack without incurring on hurt effects.

        This also re-initializes the pet, resetting exp, level, etc.

        Parameters
        ----------
        health: int
            The new health value.

        attack: int
            The new attack value.
        """
        if type(health) != int or type(attack) != int:
            raise TypeError('health and attack must be integer values')
        else:
            self.__init__()
            self._health = health
            self._attack = attack

    """
    The following functions are to be overriden according to each pet's unique
    ability. If not, the default behavior of most of these is a no-op.
    """

    #####
    # Begin shop phase only functions.
    ####

    @capture_action
    def on_buy(self, *args, **kwargs):
        """What happens when this pet is bought from the shop."""
        self._gold_cost = 1

    @capture_action
    def on_eat_food(self, *args, **kwargs):
        """What happens when this pet eats food."""
        # Trigger friends' on friend eat food abilities
        index = self._friends.index(self)
        for i in range(len(self._friends)):
            if self._friends[i]:
                self._friends[i].on_friend_eat_food(index)

    @capture_action
    def on_friend_bought(self, *args, **kwargs):
        """What happens when a friendly pet is bought."""
        pass

    @capture_action
    def on_friend_eat_food(self, *args, **kwargs):
        """What happens when a friendly pet eats food."""
        pass

    @capture_action
    def on_friend_sold(self, *args, **kwargs):
        """What happens when a friendly pet is sold."""
        pass

    @capture_action
    def on_level_up(self, *args, **kwargs):
        """What happens when this pet levels up."""
        self._gold_cost += 1

    @capture_action
    def on_sell(self, *args, **kwargs):
        """What happens when this pet is sold."""
        pass

    @capture_action
    def on_turn_end(self, *args, **kwargs):
        """What happens when the turn ends."""
        pass

    @capture_action
    def on_turn_start(self, *args, **kwargs):
        """What happens when the turn starts."""
        pass

    #####
    # Begin battle phase only functions.
    #####

    @capture_action
    def on_battle_end(self, *args, **kwargs):
        """What happens when the battle phase ends."""
        # Resets the health and attack buffs
        self._health_buff = 0
        self._attack_buff = 0

    @capture_action
    def on_battle_start(self, *args, **kwargs):
        """What happens when the battle phase starts."""
        # Grants health and attack buffs, capped at max values
        self.health += self._health_buff
        self.attack += self._attack_buff

    @capture_action
    def before_attack(self, *args, **kwargs):
        """What happens before attacking."""
        # Grant steak attack modifier
        if self._effect == 'Stk':
            self.attack += 20
            self._effect = None
        elif self._effect == 'Bne':
            self.attack += 5

    @capture_action
    def on_friend_attack(self, *args, **kwargs):
        """What happens when a friend attacks."""
        pass

    @capture_action
    def on_knock_out(self, *args, **kwargs):
        """What happens when this pet knocks out an opponent."""
        pass

    #####
    # Begin functions for either phase.
    #####

    def on_faint(self, *args, **kwargs):
        """What happens when this pet faints."""
        # Remove self from deck
        index = self._friends.index(self)
        if index != -1:  # might be missing already if action was duplicated
            del self._friends[index]

        # Trigger friends' on friend faint abilities
        for i in range(len(self._friends)):
            if self._friends[i]:
                self._friends[i].on_friend_faint(index)

        # Summon a honey bee
        if self.effect == 'Bee':
            # Lazy import to avoid circular import since the tokens
            # subclass Pet
            from gym_snape.game.pets import tokens
            self._friends.insert(index, tokens.HoneyBee())
            self._effect = None

        # Come back to life
        elif self.effect == '1up':
            replacement = deepcopy(self)
            replacement.zombify()
            self._friends[index] = replacement

    @capture_action
    def on_friend_faint(self, *args, **kwargs):
        """What happens when a friendly pet faints."""
        pass

    def on_friend_summoned(self, *args, **kwargs):
        """
        What happens when a friendly pet is summoned.

        This action is not captured since it depends only on the summon.
        """
        pass

    @capture_action
    def on_hurt(self, *args, **kwargs):
        """What happens when this pet is hurt."""
        pass
