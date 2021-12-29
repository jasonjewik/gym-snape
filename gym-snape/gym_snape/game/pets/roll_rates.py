"""
Maps tiers to roll rates for all pets at that tier and lower.
"""

# Local application imports
from gym_snape.game.utils import RollRate
from gym_snape.game.pets.tier1 import *
from gym_snape.game.pets.tier2 import *
from gym_snape.game.pets.tier3 import *
from gym_snape.game.pets.tier4 import *
from gym_snape.game.pets.tier5 import *
from gym_snape.game.pets.tier6 import *


roll_rates = {
    1: [
        RollRate(Ant, 0.12375),
        RollRate(Beaver, 0.12375),
        RollRate(Cricket, 0.12375),
        RollRate(Fish, 0.12375),
        RollRate(Horse, 0.12375),
        RollRate(Mosquito, 0.12375),
        RollRate(Otter, 0.12375),
        RollRate(Pig, 0.12375),
        RollRate(Sloth, 0.01)
    ],
    2: [
        RollRate(Ant, 0.055),
        RollRate(Beaver, 0.055),
        RollRate(Cricket, 0.055),
        RollRate(Fish, 0.055),
        RollRate(Horse, 0.055),
        RollRate(Mosquito, 0.055),
        RollRate(Otter, 0.055),
        RollRate(Pig, 0.055),
        RollRate(Sloth, 0.01),
        RollRate(Crab, 0.055),
        RollRate(Dodo, 0.055),
        RollRate(Elephant, 0.055),
        RollRate(Flamingo, 0.055),
        RollRate(Hedgehog, 0.055),
        RollRate(Peacock, 0.055),
        RollRate(Rat, 0.055),
        RollRate(Shrimp, 0.055),
        RollRate(Spider, 0.055),
        RollRate(Swan, 0.055)
    ],
    3: [
        RollRate(Ant, 0.01875),
        RollRate(Beaver, 0.01875),
        RollRate(Cricket, 0.01875),
        RollRate(Fish, 0.01875),
        RollRate(Horse, 0.01875),
        RollRate(Mosquito, 0.01875),
        RollRate(Otter, 0.01875),
        RollRate(Pig, 0.01875),
        RollRate(Sloth, 0),
        RollRate(Crab, 0.03),
        RollRate(Dodo, 0.03),
        RollRate(Elephant, 0.03),
        RollRate(Flamingo, 0.03),
        RollRate(Hedgehog, 0.03),
        RollRate(Peacock, 0.03),
        RollRate(Rat, 0.03),
        RollRate(Shrimp, 0.03),
        RollRate(Spider, 0.03),
        RollRate(Swan, 0.03),
        RollRate(Badger, 0.05),
        RollRate(BlowFish, 0.05),
        RollRate(Camel, 0.05),
        RollRate(Dog, 0.05),
        RollRate(Giraffe, 0.05),
        RollRate(Kangaroo, 0.05),
        RollRate(Ox, 0.05),
        RollRate(Rabbit, 0.05),
        RollRate(Sheep, 0.05),
        RollRate(Snail, 0.05),
        RollRate(Turtle, 0.05)
    ],
    4: [
        RollRate(Ant, 0.0095),
        RollRate(Beaver, 0.0095),
        RollRate(Cricket, 0.0095),
        RollRate(Fish, 0.0095),
        RollRate(Horse, 0.0095),
        RollRate(Mosquito, 0.0095),
        RollRate(Otter, 0.0095),
        RollRate(Pig, 0.0095),
        RollRate(Sloth, 0.004),
        RollRate(Crab, 0.0095),
        RollRate(Dodo, 0.0095),
        RollRate(Elephant, 0.0095),
        RollRate(Flamingo, 0.0095),
        RollRate(Hedgehog, 0.0095),
        RollRate(Peacock, 0.0095),
        RollRate(Rat, 0.0095),
        RollRate(Shrimp, 0.0095),
        RollRate(Spider, 0.0095),
        RollRate(Swan, 0.0095),
        RollRate(Badger, 0.03),
        RollRate(BlowFish, 0.03),
        RollRate(Camel, 0.03),
        RollRate(Dog, 0.03),
        RollRate(Giraffe, 0.03),
        RollRate(Kangaroo, 0.03),
        RollRate(Ox, 0.03),
        RollRate(Rabbit, 0.03),
        RollRate(Sheep, 0.03),
        RollRate(Snail, 0.03),
        RollRate(Turtle, 0.03),
        RollRate(Bison, 0.045),
        RollRate(Deer, 0.045),
        RollRate(Dolphin, 0.045),
        RollRate(Hippo, 0.045),
        RollRate(Parrot, 0.045),
        RollRate(Penguin, 0.045),
        RollRate(Rooster, 0.045),
        RollRate(Skunk, 0.045),
        RollRate(Squirrel, 0.045),
        RollRate(Whale, 0.045),
        RollRate(Worm, 0.045)
    ],
    5: [
        RollRate(Ant, 0.005),
        RollRate(Beaver, 0.005),
        RollRate(Cricket, 0.005),
        RollRate(Fish, 0.005),
        RollRate(Horse, 0.005),
        RollRate(Mosquito, 0.005),
        RollRate(Otter, 0.005),
        RollRate(Pig, 0.005),
        RollRate(Sloth, 0.001),
        RollRate(Crab, 0.014),
        RollRate(Dodo, 0.014),
        RollRate(Elephant, 0.014),
        RollRate(Flamingo, 0.014),
        RollRate(Hedgehog, 0.014),
        RollRate(Peacock, 0.014),
        RollRate(Rat, 0.014),
        RollRate(Shrimp, 0.014),
        RollRate(Spider, 0.014),
        RollRate(Swan, 0.014),
        RollRate(Badger, 0.014),
        RollRate(BlowFish, 0.014),
        RollRate(Camel, 0.014),
        RollRate(Dog, 0.014),
        RollRate(Giraffe, 0.014),
        RollRate(Kangaroo, 0.014),
        RollRate(Ox, 0.014),
        RollRate(Rabbit, 0.014),
        RollRate(Sheep, 0.014),
        RollRate(Snail, 0.014),
        RollRate(Turtle, 0.014),
        RollRate(Bison, 0.035),
        RollRate(Deer, 0.035),
        RollRate(Dolphin, 0.035),
        RollRate(Hippo, 0.035),
        RollRate(Parrot, 0.035),
        RollRate(Penguin, 0.035),
        RollRate(Rooster, 0.035),
        RollRate(Skunk, 0.035),
        RollRate(Squirrel, 0.035),
        RollRate(Whale, 0.035),
        RollRate(Worm, 0.035),
        RollRate(Cow, 0.035),
        RollRate(Crocodile, 0.035),
        RollRate(Monkey, 0.035),
        RollRate(Rhino, 0.035),
        RollRate(Scorpion, 0.035),
        RollRate(Seal, 0.035),
        RollRate(Shark, 0.035),
        RollRate(Turkey, 0.035)
    ],
    6: [
        RollRate(Ant, 0.0035),
        RollRate(Beaver, 0.0035),
        RollRate(Cricket, 0.0035),
        RollRate(Fish, 0.0035),
        RollRate(Horse, 0.0035),
        RollRate(Mosquito, 0.0035),
        RollRate(Otter, 0.0035),
        RollRate(Pig, 0.0035),
        RollRate(Sloth, 0),
        RollRate(Crab, 0.0035),
        RollRate(Dodo, 0.0035),
        RollRate(Elephant, 0.0035),
        RollRate(Flamingo, 0.0035),
        RollRate(Hedgehog, 0.0035),
        RollRate(Peacock, 0.0035),
        RollRate(Rat, 0.002),
        RollRate(Shrimp, 0.0035),
        RollRate(Spider, 0.0035),
        RollRate(Swan, 0.0035),
        RollRate(Badger, 0.0035),
        RollRate(BlowFish, 0.0035),
        RollRate(Camel, 0.0035),
        RollRate(Dog, 0.0035),
        RollRate(Giraffe, 0.0035),
        RollRate(Kangaroo, 0.0035),
        RollRate(Ox, 0.0035),
        RollRate(Rabbit, 0.0035),
        RollRate(Sheep, 0.0035),
        RollRate(Snail, 0.0035),
        RollRate(Turtle, 0.0035),
        RollRate(Bison, 0.02),
        RollRate(Deer, 0.02),
        RollRate(Dolphin, 0.02),
        RollRate(Hippo, 0.02),
        RollRate(Parrot, 0.02),
        RollRate(Penguin, 0.02),
        RollRate(Rooster, 0.02),
        RollRate(Skunk, 0.02),
        RollRate(Squirrel, 0.02),
        RollRate(Whale, 0.02),
        RollRate(Worm, 0.02),
        RollRate(Cow, 0.04),
        RollRate(Crocodile, 0.04),
        RollRate(Monkey, 0.04),
        RollRate(Rhino, 0.04),
        RollRate(Scorpion, 0.04),
        RollRate(Seal, 0.04),
        RollRate(Shark, 0.04),
        RollRate(Turkey, 0.04),
        RollRate(Boar, 0.04),
        RollRate(Cat, 0.04),
        RollRate(Dragon, 0.04),
        RollRate(Fly, 0.04),
        RollRate(Gorilla, 0.04),
        RollRate(Leopard, 0.04),
        RollRate(Mammoth, 0.04),
        RollRate(Snake, 0.04),
        RollRate(Tiger, 0.04)
    ]
}


if __name__ == '__main__':
    """Check that all roll rates are valid."""
    # Lazy import since we only need numpy for this test
    import numpy as np
    for i in sorted(roll_rates.keys()):
        pets, rates = [], []
        for rr in roll_rates[i]:
            pets.append(rr.item)
            rates.append(rr.rate)
        try:
            np.random.choice(pets, p=rates, size=1)
        except:
            print(f'Could not sample from tier {i}')
            print(f'Summed to {np.sum(rates)}')