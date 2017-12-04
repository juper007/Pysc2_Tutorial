from pysc2.env import sc2_env

import sys
from absl import flags

from pysc2.lib import actions as sc2_actions
from pysc2.env import environment as sc2_environment
from pysc2.lib import features as sc2_features
import numpy as np
import time

# Feature
_UNIT_TYPE =sc2_features.SCREEN_FEATURES.unit_type.index  # "6"
_PLAYER_RELATIVE = sc2_features.SCREEN_FEATURES.player_relative.index  # "5"

# Action
_NO_OP = sc2_actions.FUNCTIONS.no_op.id
_SELECT_POINT = sc2_actions.FUNCTIONS.select_point.id
_SELECT_UNIT = sc2_actions.FUNCTIONS.select_unit.id
_RIGHT_CLICK = sc2_actions.FUNCTIONS.Smart_screen.id

# Unit
_TERRAN_MARINE = 48

# PARAM
_NOT_QUEUED = [0]


step_mul = 16
steps = 400


def main():
    with sc2_env.SC2Env(map_name="MoveToBeacon",
                        step_mul=step_mul,
                        visualize=True,
                        game_steps_per_episode=steps * step_mul) as env:

        for _ in range(10):
            obs = env.reset()

            done = False
            agent_selected = False
            agent_moving = False

            while not done:
                # time.sleep(0.5)

                player_relative = obs[0].observation["screen"][_PLAYER_RELATIVE]
                unit_type = obs[0].observation["screen"][_UNIT_TYPE]

                agent_y, agent_x = (unit_type == _TERRAN_MARINE).nonzero()
                target_y, target_x = (unit_type == 317).nonzero()



                if agent_y.size == 0 or agent_x.size == 0:
                    obs = env.step(actions=[sc2_actions.FunctionCall(_NO_OP, [])])
                    continue

                agent_location = [agent_x[0], agent_y[0]]
                if not agent_selected:
                    agent_selected = True
                    obs = env.step(actions=[sc2_actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, agent_location])])
                elif not agent_moving:
                    target = [target_x[0]+2, target_y[0]+2]
                    # direction = np.random.randint(4)
                    # if direction == 0:
                    #     target = move_up(agent_location)
                    # elif direction == 1:
                    #     target = move_down(agent_location)
                    # elif direction == 2:
                    #     target = move_left(agent_location)
                    # else:
                    #     target = move_down(agent_location)

                    agent_moving = True
                    obs = env.step(actions=[sc2_actions.FunctionCall(_RIGHT_CLICK, [_NOT_QUEUED, target])])
                else:
                    if agent_location == target:
                        agent_moving = False
                    obs = env.step(actions=[sc2_actions.FunctionCall(_NO_OP, [])])

                done = obs[0].step_type == sc2_environment.StepType.LAST
                reward = obs[0].reward
                print(done, reward)
                # obs = env.step(actions=[sc2_actions.FunctionCall(_NO_OP, [])])


def move_up(location):
    if location[1] < 4:
        return location
    else:
        return [location[0], location[1] - 2]


def move_down(location):
    if location[1] > 42:
        return location
    else:
        return [location[0], location[1] + 2]


def move_left(location):
    if location[0] < 2:
        return location
    else:
        return [location[0] - 2, location[1]]


def move_right(location):
    if location[0] > 58:
        return location
    else:
        return [location[0] + 2, location[1]]


if __name__ == '__main__':
    FLAGS = flags.FLAGS
    FLAGS(sys.argv)
    main()
