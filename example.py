"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck import sensors


def uav_example():
    """A basic example of how to use the UAV agent."""
    env = holodeck.make("UrbanCity-MaxDistance")

    # This line can be used to change the control scheme for an agent
    # env.agents["uav0"].set_control_scheme(ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

    for i in range(10):
        env.reset()

        # This command tells the UAV to not roll or pitch, but to constantly yaw left at
        # 10m altitude.
        command = np.array([0, 0, 2, 1000])
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)
            # To access specific sensor data:
            pixels = state["RGBCamera"]
            velocity = state["VelocitySensor"]
            # For a full list of sensors the UAV has, consult the configuration file
            # "InfiniteForest-MaxDistance.json"

    # You can control the AgentFollower camera (what you see) by pressing V to toggle spectator
    # mode. This detaches the camera and allows you to move freely about the world.
    # You can also press C to snap to the location of the camera to see the world from the
    # perspective of the agent. See the Controls section of the ReadMe for more details.


def sphere_example():
    """A basic example of how to use the sphere agent."""
    env = holodeck.make("MazeWorld-FinishMazeSphere")

    # This command is to constantly rotate to the right
    command = 2
    for i in range(10):
        env.reset()
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the sphere robot has, view the README


def android_example():
    """A basic example of how to use the android agent."""
    env = holodeck.make("AndroidPlayground-MaxDistance")

    # The Android's command is a 94 length vector representing torques to be applied at each
    # of his joints
    command = np.ones(94) * 10
    for i in range(10):
        env.reset()
        for j in range(1000):
            if j % 50 == 0:
                command *= -1

            state, reward, terminal, _ = env.step(command)
            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the android has, view the README


def multi_agent_example():
    """A basic example of using multiple agents"""
    env = holodeck.make("CyberPunkCity-Follow")

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([0, 0, 0])
    for i in range(10):
        env.reset()
        env.tick()
        env.act("uav0", cmd0)
        env.act("nav0", cmd1)
        for _ in range(1000):
            states = env.tick()

            pixels = states["uav0"]["RGBCamera"]
            location = states["uav0"]["LocationSensor"]

            task = states["uav0"]["FollowTask"]
            reward = task[0]
            terminal = task[1]


def world_command_examples():
    """A few examples to showcase commands for manipulating the worlds."""
    env = holodeck.make("MazeWorld-FinishMazeSphere")

    # This is the unaltered MazeWorld
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_day_time_command sets the hour between 0 and 23 (military time).
    # This example sets it to 6 AM.
    env.weather.set_day_time(6)
    for _ in range(300):
        _ = env.tick()
    env.reset()  # reset() undoes all alterations to the world

    # The start_day_cycle command starts rotating the sun to emulate day cycles.
    # The parameter sets the day length in minutes.
    env.weather.start_day_cycle(5)
    for _ in range(1500):
        _ = env.tick()
    env.reset()

    # The set_fog_density changes the density of the fog in the world. 1 is the maximum density.
    env.weather.set_fog_density(0.25)
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_weather_command changes the weather in the world. The two available options are "rain"
    # and "cloudy". The rainfall particle system is attached to the agent, so the rain particles will
    # only be found around each agent. Every world is clear by default.
    env.weather.set_weather("rain")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.weather.set_weather("cloudy")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.move_viewport([1000, 1000, 1000], [0, 0, 0])
    for _ in range(500):
        _ = env.tick()
    env.reset()


def editor_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine Editor. Most people that use holodeck will not need this.

    This example uses a custom scenario, see
    https://holodeck.readthedocs.io/en/latest/usage/examples/custom-scenarios.html

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """

    # config = {
    #     "name": "test",
    #     "world": "TestWorld",
    #     "main_agent": "sphere0",
    #     "agents": [
    #         {
    #             "agent_name": "sphere0",
    #             "agent_type": "SphereAgent",
    #             "sensors": [
    #                 # {"sensor_type": "LocationSensor"},
    #                 # {"sensor_type": "VelocitySensor"},
    #                 {"sensor_type": "RGBCamera"},
    #             ],
    #             "control_scheme": 1,
    #             "location": [0, 0, 1],
    #         }
    #     ],
    # }

    config = {
        "name": "test",
        "world": "TestWorld",
        "main_agent": "duckiebot_0",
        "agents": [
            {
                "agent_name": "duckiebot_0",
                "agent_type": "DuckiebotAgent",
                "sensors": [
                    # {"sensor_type": "LocationSensor"},
                    # {"sensor_type": "VelocitySensor"},
                    {
                        "sensor_type": "RGBCamera",
                        "sensor_name": "RGBCamera",
                        "existing": True,
                        "configuration": {
                            "CaptureHeight": 84,
                            "CaptureWidth": 84,
                        }
                    },
                    {
                        "sensor_type": "DuckiebotsSemanticMaskCamera",
                        "sensor_name": "DuckiebotsSemanticMaskCamera",
                        "existing": True,
                        "configuration": {
                            "CaptureHeight": 84,
                            "CaptureWidth": 84,
                        }
                    },
                    {
                        "sensor_type": "DuckiebotsLoopStatusSensor",
                        "sensor_name": "DuckiebotsLoopStatusSensor",
                        "existing": True,
                    },
                ],
                "control_scheme": 1,
                "location": [0, 0, 1],
            }
        ],
    }

    print("--launching env--")
    env = HolodeckEnvironment(scenario=config, start_world=False)
    print("--env launch complete--")
    command = [1, 1]

    from duckiebots_unreal_sim.tools.image_renderer import ImageRenderer

    renderer1 = ImageRenderer(height=84, width=84)
    renderer2 = ImageRenderer(height=84, width=84)

    try:
        while True:
            env.reset()
            env.send_world_command(name="RandomizeDuckiebotsWorld",
                                   num_params=[],
                                   string_params=[
                                       "C:\Users\\author1\Documents\GitHub\duckiebotssim\PythonInterface\duckiebots_unreal_sim\\backdrop_movies\movie_batch_1.bk2",
                                       "C:\Users\\author1\Documents\GitHub\duckiebotssim\PythonInterface\duckiebots_unreal_sim\\road_movies\\road_texture.bk2"
                                   ])
            for _ in range(1000):
                state, reward, terminal, _ = env.step(command)
                # if state["DuckiebotsLoopStatusSensor"][3]:
                #     print(f"entered new road tile")
                # if "RGBCamera" in state:
                #     print(state["RGBCamera"])
                #     renderer1.render_cv2_image(state["RGBCamera"][::-1, :, :3])
                # if "DuckiebotsSemanticMaskCamera" in state:
                #     renderer2.render_cv2_image(state["DuckiebotsSemanticMaskCamera"][::-1, :, :3])

                # print(state["DuckiebotsLoopStatusSensor"])
                if state["DuckiebotsLoopStatusSensor"][0]:
                    print(f"hit white line")

                if state["DuckiebotsLoopStatusSensor"][1]:
                    print(f"hit yellow line")
                # print(f"state shape: {state.shape}. {np.mean(state)}")
    finally:
        renderer1.close()
        renderer2.close()


def editor_multi_agent_example():
    """This editor example shows how to interact with holodeck worlds that have multiple agents.
    This is specifically for when working with UE4 directly and not a prebuilt binary.

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """
    config = {
        "name": "test_handagent",
        "world": "TestWorld",
        "main_agent": "hand0",
        "agents": [
            {
                "agent_name": "uav0",
                "agent_type": "UavAgent",
                "sensors": [],
                "control_scheme": 1,
                "location": [0, 0, 1],
            },
            {
                "agent_name": "uav1",
                "agent_type": "UavAgent",
                "sensors": [],
                "control_scheme": 1,
                "location": [0, 0, 5],
            },
        ],
    }

    env = HolodeckEnvironment(scenario=config, start_world=False)

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([0, 0, 5, 10])

    for i in range(10):
        env.reset()
        env.act("uav0", cmd0)
        env.act("uav1", cmd1)
        for _ in range(1000):
            states = env.tick()


if __name__ == '__main__':
    editor_example()