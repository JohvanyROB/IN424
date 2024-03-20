import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():
    simu_pkg = get_package_share_directory("in424_simu")
    gazebo_pkg = get_package_share_directory("gazebo_ros")

    os.environ["GAZEBO_MODEL_PATH"] += os.path.join(simu_pkg, "models")

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg, "launch", "gazebo.launch.py")
        )
    )

    spawn_robots_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(simu_pkg, "launch", "spawn_robots_launch.py")
        )
    )

    stop_previous_gazebo = ExecuteProcess(cmd=[
        "killall",
        "gzserver",
        "gzclient"
    ], output='screen')


    return LaunchDescription([
        DeclareLaunchArgument(
            "world",
            default_value = os.path.join(simu_pkg, "worlds", "env.world"),
            description = "World file to use for the simulation"
        ),

        stop_previous_gazebo,

        RegisterEventHandler(
            event_handler = OnProcessExit(
              target_action = stop_previous_gazebo,
              on_exit = [gazebo_launch]  #start this node when previous gazebo processes have been stopped
            )
        ),

        TimerAction(
           period = 5.0,
           actions = [
                spawn_robots_launch
           ]
        ),

        Node(
            package = "rviz2",
            executable = "rviz2",
            arguments = ["-d", os.path.join(simu_pkg, "cfg", "config.rviz")]
        )
    ])
