"""Example usage of SNAPE with two agents that act randomly."""

# Local application imports
from agents.random import RandomAgent
from gym_snape import Snape

# Initialize player 1 and their environment
env1 = Snape()
env1.reset()
p1 = RandomAgent(env1)

# Initialize player 2 and their environment
env2 = Snape()
env2.reset()
p2 = RandomAgent(env2)

# Assign opponent
env1.assign_opponent(env2)
env2.assign_opponent(env1)

# Have the agents compete (each can force the other to battle whenever)
done = False
max_actions = 10_000
n_actions1, n_actions2 = 1, 1
while not done:
    act1 = p1.select_action()
    # print(f'P1\'s action #{n_actions1}: {act1}')
    obs1, rew1, done1, info1 = env1.step(act1)
    n_actions1 = obs1['n_actions']
    act2 = p2.select_action()
    # print(f'P2\'s action #{n_actions2}: {act2}')
    obs2, rew2, done2, info2 = env2.step(act2)
    n_actions2 = obs2['n_actions']
    done = done1 or done2 or n_actions1 > max_actions or n_actions2 > max_actions

# View results
print('PLAYER 1')
print(env1.game)

print('PLAYER 2')
print(env2.game)
