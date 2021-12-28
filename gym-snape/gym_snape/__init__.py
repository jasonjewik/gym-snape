from gym.envs.registration import register
from gym_snape.env import Snape

id = 'snape-v0'
register(
    id=id,
    entry_point='gym_snape:Snape',
)
