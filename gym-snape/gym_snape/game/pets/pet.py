# Standard library imports
import typing
from typing import Final, Optional

# Local application imports
from gym_snape.game import effects


class Pet:
    """The base class for pets."""

    def __init__(self):
        self._MAX_ATTACK: Final = 50
        self._MAX_HEALTH: Final = 50
        self._EXP_TO_LEVEL_UP: Final = (2, 3)
        self._MAX_LEVEL: Final = len(self._EXP_TO_LEVEL_UP) + 1

        self._health = 0
        self._health_buff = 0

        self._attack = 0
        self._attack_buff = 0

        self._level = 1
        self.experience = 0

        self._gold_cost = 3
        self.effect = None

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
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        if type(value) == int:
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

    @typing.final
    def assign_game(self, game):
        """Assigns a game to this pet."""
        self._game = game

    @typing.final
    def assign_friends(self, deck):
        """Assigns a friendly deck to this pet."""
        self._friends = deck

    @typing.final
    def assign_enemies(self, deck):
        """Assigns an enemy deck to this pet."""
        self._enemies = deck

    @typing.final
    def can_level(self) -> bool:
        """True if this pet's level is less than the max level."""
        return self.level < self._MAX_LEVEL

    """
    The following functions are to be overriden according to each pet's unique
    ability. If not, the default behavior of most of these is a no-op.
    """

    def on_buy(self, *args, **kwargs):
        """What happens when this pet is bought from the shop."""
        pass

    def on_sell(self, *args, **kwargs):
        """What happens when this pet is sold."""
        pass

    def on_consume_food(self, *args, **kwargs):
        """What happens when this pet consumes food."""
        pass

    def on_faint(self, *args, **kwargs):
        """What happens when this pet faints."""
        # Remove self from deck
        for i in range(len(self._friends)):
            if id(self._friends[i]) == id(self):
                del self._friends[i]
                # Summon a honey bee
                if self.effect == 'Bee':
                    # Lazy import to avoid circular import since the tokens
                    # subclass Pet
                    from gym_snape.game.pets import tokens
                    self._friends[i] = tokens.HoneyBee()

    def on_friend_bought(self, *args, **kwargs):
        """What happens when a friendly pet is bought."""
        pass

    def on_friend_sold(self, *args, **kwargs):
        """What happens when a friendly pet is sold."""
        pass

    def on_friend_summoned(self, *args, **kwargs):
        """What happens when a friendly pet is summoned."""
        pass

    def on_friend_faint(self, *args, **kwargs):
        """What happens when a friendly pet faints."""
        pass

    def before_attack(self, *args, **kwargs):
        """What happens before attacking."""
        pass

    def on_friend_attack(self, *args, **kwargs):
        """What happens when a friend attacks."""
        pass

    def on_turn_start(self, *args, **kwargs):
        """What happens when the turn starts."""
        pass

    def on_turn_end(self, *args, **kwargs):
        """What happens when the turn ends."""
        pass

    def on_battle_start(self, *args, **kwargs):
        """What happens when the battle phase starts."""
        # Grants health and attack buffs, capped at max values
        self.health += self._health_buff
        self.attack += self._attack_buff

    def on_battle_end(self, *args, **kwargs):
        """What happens when the battle phase ends."""
        # Resets the health and attack buffs
        self._health_buff = 0
        self._attack_buff = 0

    def on_hurt(self, *args, **kwargs):
        """What happens when this pet is hurt."""
        pass

    def on_knock_out(self, *args, **kwargs):
        """What happens when this pet knocks out an opponent."""
        pass

    def on_eat_food(self, *args, **kwargs):
        """What happens when this pet eats food."""
        pass

    def on_level_up(self, *args, **kwargs):
        """What happens when this pet levels up."""
        pass
