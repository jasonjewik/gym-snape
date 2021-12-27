from gym_snape.game.pets.pet import Pet


class HoneyBee(Pet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Has attack and health of 1."""
        self._name = 'HONEY BEE'
        self.attack = 1
        self.health = 1


class ZombieCricket(Pet):
    def __init__(self, parent, *args, **kwargs):
        """Has attack/health = to parent's level."""
        super().__init__(*args, **kwargs)
        self._name = 'ZOMBIE CRICKET'
        self.attack = parent.level
        self.health = parent.level
