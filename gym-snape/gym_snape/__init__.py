from gym.envs.registration import register

register(
    id='snape-v0',
    entry_point='gym_snape.envs:GameEnv',
)
