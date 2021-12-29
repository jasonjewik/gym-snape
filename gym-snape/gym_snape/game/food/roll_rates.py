"""
Maps tiers to roll rates for all food items at that tier and lower.
"""

# Local application imports
from gym_snape.game.utils import RollRate
from gym_snape.game.food.tier1 import *
from gym_snape.game.food.tier2 import *
from gym_snape.game.food.tier3 import *
from gym_snape.game.food.tier4 import *
from gym_snape.game.food.tier5 import *
from gym_snape.game.food.tier6 import *

roll_rates = {
    1: [
        RollRate(Apple, 0.5),
        RollRate(Honey, 0.5)
    ],
    2: [
        RollRate(Apple, 0.2),
        RollRate(Honey, 0.2),
        RollRate(Cupcake, 0.2),
        RollRate(MeatBone, 0.2),
        RollRate(SleepingPill, 0.2)
    ],
    3: [
        RollRate(Apple, 0.1),
        RollRate(Honey, 0.15),
        RollRate(Cupcake, 0.15),
        RollRate(MeatBone, 0.15),
        RollRate(SleepingPill, 0.15),
        RollRate(Garlic, 0.15),
        RollRate(SaladBowl, 0.15)
    ],
    4: [
        RollRate(Apple, 0),
        RollRate(Honey, 0.05),
        RollRate(Cupcake, 0.05),
        RollRate(MeatBone, 0.15),
        RollRate(SleepingPill, 0.15),
        RollRate(Garlic, 0.15),
        RollRate(SaladBowl, 0.15),
        RollRate(CannedFood, 0.15),
        RollRate(Pear, 0.15)
    ],
    5: [
        RollRate(Apple, 0),
        RollRate(Honey, 0),
        RollRate(Cupcake, 0),
        RollRate(MeatBone, 0.1),
        RollRate(SleepingPill, 0.1),
        RollRate(Garlic, 0.1),
        RollRate(SaladBowl, 0.1),
        RollRate(CannedFood, 0.12),
        RollRate(Pear, 0.12),
        RollRate(Chili, 0.12),
        RollRate(Chocolate, 0.12),
        RollRate(Sushi, 0.12)
    ],
    6: [
        RollRate(Apple, 0),
        RollRate(Honey, 0),
        RollRate(Cupcake, 0),
        RollRate(MeatBone, 0),
        RollRate(SleepingPill, 0),
        RollRate(Garlic, 0.05),
        RollRate(SaladBowl, 0.05),
        RollRate(CannedFood, 0.1),
        RollRate(Pear, 0.1),
        RollRate(Chili, 0.1),
        RollRate(Chocolate, 0.1),
        RollRate(Sushi, 0.1),
        RollRate(Melon, 0.1),
        RollRate(Mushroom, 0.1),
        RollRate(Pizza, 0.1),
        RollRate(Steak, 0.1)
    ]
}

if __name__ == '__main__':
    """Check that all roll rates are valid."""
    # Lazy import since only need numpy for this test
    import numpy as np
    for i in sorted(roll_rates.keys()):
        food, rates = [], []
        for rr in roll_rates[i]:
            food.append(rr.item)
            rates.append(rr.rate)
        try:
            np.random.choice(food, p=rates, size=1)
        except:
            print(f'Could not sample from tier {i}')
            print(f'Summed to {np.sum(rates)}')
