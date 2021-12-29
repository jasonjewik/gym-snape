"""
Definitions of the tokens: Bus, Chick, Dirty Rat, Honey Bee, Ram, 
Zombie Cricket, and Zombie Fly.
"""

# Standard library imports
import math

# Local application imports
from gym_snape.game.pets import Pet


class Bus(Pet):
    def __init__(self, parent):
        super().__init__()
        self._name = 'BUS'
        self.attack = 5 * parent.level
        self.health = 5 * parent.level
        self.effect = 'Spl'


class Chick(Pet):
    def __init__(self, parent):
        super().__init__()
        self._name = 'CHICK'
        self.attack = math.floor(parent.attack / 2)
        self.health = 1


class DirtyRat(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'DIRTY RAT'
        self.attack = 1
        self.health = 1


class HoneyBee(Pet):
    def __init__(self):
        super().__init__()
        self._name = 'HONEY BEE'
        self.attack = 1
        self.health = 1


class Ram(Pet):
    def __init__(self, parent):
        super().__init__()
        self._name = 'RAM'
        self.attack = 2 * parent.level
        self.health = 2 * parent.level


class ZombieCricket(Pet):
    def __init__(self, parent):
        super().__init__()
        self._name = 'Z-CRICKET'
        self.attack = parent.level
        self.health = parent.level


class ZombieFly(Pet):
    def __init__(self, parent):
        super().__init__()
        self._name = 'Z-FLY'
        self.attack = 5 * parent.level
        self.health = 5 * parent.level
