# Standard library imports
from collections import namedtuple
from enum import IntEnum


class MatchResult(IntEnum):
    WON = 0
    DRAW = 1
    LOST = 2


RollRate = namedtuple('RollRate', ['item', 'rate'])
