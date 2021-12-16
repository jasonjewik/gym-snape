from gym.envs.registration import register

id = 'snape-v0'
register(
    id=id,
    entry_point='gym_snape.envs:GameEnv',
)
