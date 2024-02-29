import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    simu_pkg = get_package_share_directory("in424_simu")

    os.environ["GAZEBO_MODEL_PATH"] += os.path.join(simu_pkg, "models")

    spawn_robots_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(simu_pkg, "launch", "spawn_robots_launch.py")
        )
    )

    return LaunchDescription([
        ExecuteProcess(cmd=[
            'gazebo',
            # '--verbose',
            '-s', 'libgazebo_ros_init.so',  # Publish /clock
            '-s', 'libgazebo_ros_factory.so',  # Provide gazebo_ros::Node
            os.path.join(simu_pkg, "worlds", "env.world")
        ], output='screen'),

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
