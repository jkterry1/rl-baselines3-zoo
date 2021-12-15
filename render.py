from stable_baselines3 import PPO
import supersuit as ss
import numpy as np
import os
import sys
from array2gif import write_gif
import sumo_rl
from pettingzoo.utils.conversions import from_parallel


#import pyglet

#pyglet.options['headless'] = True
num = sys.argv[1]


# def image_transpose(env):
#     if is_image_space(env.observation_space) and not is_image_space_channels_first(env.observation_space):
#         env = VecTransposeImage(env)
#     return env

RESOLUTION = (4000, 4000)

n_agents = 7

env = sumo_rl.ingolstadt7(sumo_warnings=False, virtual_display=RESOLUTION)
env = from_parallel(env)
env = ss.pad_observations_v0(env)
env = ss.pad_action_space_v0(env)

policies = os.listdir("./mature_policies/" + str(num) + "/")

for policy in policies:
    model = PPO.load("./mature_policies/" + str(num) + "/" + policy)

    for j in ['a','b','c','d','e']:

        obs_list = []
        i = 0
        env.reset()
        total_reward = 0

        while True:
            for agent in env.agent_iter():
                observation, reward, done, _ = env.last()
                action = (model.predict(observation, deterministic=True)[0] if not done else None)
                total_reward += reward

                env.step(action)
                i += 1
                if i % (len(env.possible_agents) + 1) == 0:
                    obs_list.append(
                        np.transpose(env.render(mode="rgb_array"), axes=(1, 0, 2))
                    )

            break

        total_reward = total_reward / n_agents

        if total_reward > -.1:
            print("writing gif")
            write_gif(
                obs_list, "./mature_gifs/" + num + "_" + policy.split("_")[0] + j + '_' + str(total_reward)[:5] + ".gif", fps=50
            )

env.close()
