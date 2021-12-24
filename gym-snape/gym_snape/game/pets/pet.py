class Pet:
    def __init__(self):
        self.MAX_ATTACK = 50
        self.MAX_HEALTH = 50
        self.EXP_TO_LEVEL_UP = (2, 3)
        self.MAX_LEVEL = len(self.EXP_TO_LEVEL_UP) + 1

        self.experience = 0
        self._level = 1
        self.tokens = []

    def __str__(self):
        name = str(type(self)).split('.')[-1].split("'")[0]
        return f'{name}: ({self.health}, {self.attack})'

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = min(value, self.MAX_HEALTH)
        if self.health <= 0:
            self.on_faint()

    def is_alive(self):
        return self.health > 0

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = min(value, self.MAX_ATTACK)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
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

    def assign_deck(self, deck):
        self._deck = deck

    def can_level(self):
        return self.level < self.MAX_LEVEL

    def on_buy(self):
        """What happens when this pet is bought from the shop."""
        pass

    def on_sell(self):
        """What happens when this pet is sold."""
        pass

    def on_faint(self):
        """What happens when this pet faints."""
        index = -1
        for i in range(len(self._deck)):
            if self._deck[i] == self:
                index = i
                del self._deck[i]

    def on_friend_bought(self):
        """What happens when a friendly pet is bought."""
        pass

    def on_friend_sold(self):
        """What happens when a friendly pet is sold."""
        pass

    def on_friend_summoned(self):
        """What happens when a friendly pet is summoned."""
        pass

    def on_friend_faint(self):
        """What happens when a friendly pet faints."""
        pass

    def before_attack(self):
        """What happens before attacking."""
        pass

    def on_friend_attack(self):
        """What happens when a friend attacks."""
        pass

    def on_turn_start(self):
        """What happens when the turn starts."""
        pass

    def on_turn_end(self):
        """What happens when the turn ends."""
        pass

    def on_battle_start(self):
        """What happens when the battle phase starts."""
        pass

    def on_battle_end(self):
        """What happens when the battle phase ends."""
        pass

    def on_hurt(self):
        """What happens when this pet is hurt."""
        pass

    def on_knock_out(self):
        """What happens when this pet knocks out an opponent."""
        pass

    def on_eat_food(self):
        """What happens when this pet eats food."""
        pass

    def on_level_up(self):
        """What happens when this pet levels up."""
        pass
