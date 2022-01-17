"""Example usage of SNAPE with simple agents."""

# Standard library imports
from argparse import ArgumentParser
from typing import Optional

# Local application imports
from agents.random import Random
from agents.rbc import RuleBasedController as RBC
from gym_snape import Snape


def main(agent_type: str, max_actions: Optional[int] = None):
    """
    Parameters
    ----------
    agent_type: str
        What type of agent to use: random or rule-based controller.
    max_actions: int
        The max number of actions to allow. Default is None, which means the
        agents will compete until one wins.
    """
    # Initialize player 1 and their environment
    env1 = Snape()
    obs1 = env1.reset()
    if agent_type == 'random':
        p1 = Random(env1)
    elif agent_type == 'rbc':
        p1 = RBC(env1)
    else:
        raise NotImplementedError(f'agent type {agent_type} is not implemented')

    # Initialize player 2 and their environment
    env2 = Snape()
    obs2 = env2.reset()
    if agent_type == 'random':
        p2 = Random(env2)
    elif agent_type == 'rbc':
        p2 = RBC(env2)
    else:
        raise NotImplementedError(f'agent type {agent_type} is not implemented')

    # Assign opponent
    env1.assign_opponent(env2)
    env2.assign_opponent(env1)

    # Have the agents compete (each can force the other to battle whenever)
    done = False
    while not done:
        # Player 1 acts
        act1 = p1.select_action(obs1)
        n_actions1 = obs1['n_actions']
        obs1, rew1, done1, info1 = env1.step(act1)

        # Player 2 acts
        act2 = p2.select_action(obs2)
        n_actions2 = obs2['n_actions']
        obs2, rew2, done2, info2 = env2.step(act2)

        # Check game over conditions
        if max_actions:
            max_actions_exceeded = n_actions1 > max_actions or n_actions2 > max_actions
        else:
            max_actions_exceeded = False
        done = done1 or done2 or max_actions_exceeded

    # View results
    print('PLAYER 1')
    print(env1.game)

    print('PLAYER 2')
    print(env2.game)


if __name__ == '__main__':
    parser = ArgumentParser(description='Example usage of SNAPE with simple agents.')
    parser.add_argument('--agent', choices=['random', 'rbc'], default='random')
    parser.add_argument('--max_actions', type=int, default=10_000)
    args = parser.parse_args()

    main(args.agent, args.max_actions)
