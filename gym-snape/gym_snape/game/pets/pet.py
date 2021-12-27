from gym_snape.game.effects import effects


class Pet:
    def __init__(self):
        self.MAX_ATTACK = 50
        self.MAX_HEALTH = 50
        self.EXP_TO_LEVEL_UP = (2, 3)
        self.MAX_LEVEL = len(self.EXP_TO_LEVEL_UP) + 1

        self._level = 1
        self._health = 0
        self._attack = 0
        self.experience = 0
        self.effect = None
        self._health_buff = 0
        self._attack_buff = 0

    def __str__(self):
        width = 10

        health_str = str(self.health+self.health_buff)
        attack_str = str(self.attack+self.attack_buff)
        if self.health_buff != 0:
            health_str = f'({health_str})'
        if self.attack_buff != 0:
            attack_str = f'({attack_str})'

        if self.effect is None:
            effect = '...'
        else:
            effect = self.effect

        exp_as_frac = f'{self.experience}/{self.EXP_TO_LEVEL_UP[self.level-1]}'

        result = (
            f'+----------+\n'
            f'|{self._name[:width]:{width}}|\n'
            f'|hp:  {health_str:{width-5}}|\n'
            f'|atk: {attack_str:{width-5}}|\n'
            f'|fct: {effect:<{width-5}}|\n'
            f'|exp: {exp_as_frac:{width-5}}|\n'
            f'|lvl: {self.level:<{width-5}}|\n'
            '+----------+\n'
        )
        return result

    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError(f'{other} is not of type {type(self)}')
        else:
            self.experience += other.experience + 1
            self.health = max(self.health, other.health) + 1
            self.attack = max(self.attack, other.attack) + 1

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

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        try:
            value = int(value)
        except:
            raise ValueError('argument must be castable to integer')
        prev_health = self.health
        self._health = min(value, self.MAX_HEALTH)
        if self.health <= 0:
            self.on_faint()
        elif self.health < prev_health:
            self.on_hurt()

    @property
    def health_buff(self):
        return self._health_buff

    @health_buff.setter
    def health_buff(self, value):
        try:
            value = int(value)
        except:
            raise TypeError('argument must be castable to integer')
        self._health_buff = value

    @property
    def attack_buff(self):
        return self._attack_buff

    @attack_buff.setter
    def attack_buff(self, value):
        try:
            value = int(value)
        except:
            raise TypeError('argument must be castable to integer')
        self._attack_buff = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        try:
            value = int(value)
        except:
            raise TypeError('argument must be castable to integer')
        self._attack = min(value, self.MAX_ATTACK)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        try:
            value = int(value)
        except:
            raise TypeError('argument must be castable to integer')
        self._experience = value
        while True:
            index = self.level - 1
            if index >= len(self.EXP_TO_LEVEL_UP):
                break
            else:
                exp_needed = self.EXP_TO_LEVEL_UP[self.level-1]
                if self.experience >= exp_needed and self.level < self.MAX_LEVEL:
                    self._level += 1
                    self._experience -= exp_needed
                    self.on_level_up()
                else:
                    break
        if self.level == self.MAX_LEVEL:
            self._experience = self.EXP_TO_LEVEL_UP[-1]

    @property
    def level(self):
        return self._level

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value):
        if value is None or value in effects:
            self._effect = value
        else:
            raise ValueError(f'{value} not in {effects}')

    def assign_friends(self, deck):
        self._friends = deck

    def assign_enemies(self, deck):
        self._enemies = deck

    def assign_game(self, game):
        self._game = game

    def can_level(self):
        return self.level < self.MAX_LEVEL

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
        for i in range(len(self._friends)):
            if id(self._friends[i]) == id(self):
                del self._friends[i]
                if self.effect == 'Bee':
                    import gym_snape.game.pets.tokens as tokens
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
        self.health += self._health_buff
        self.attack += self._attack_buff

    def on_battle_end(self, *args, **kwargs):
        """What happens when the battle phase ends."""
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
