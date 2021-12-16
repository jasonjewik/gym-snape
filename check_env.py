"""
A script for quickly testing the game environment.
"""

import gym
import sys
import gym_snape

config = 'configs/default'
for i, arg in enumerate(sys.argv):
    if arg == '--config':
        config = sys.argv[i+1]

env = gym.make(f'gym_snape:{gym_snape.id}', config=config)
env.render(mode='ansi')
