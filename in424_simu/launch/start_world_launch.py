import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():
    gazebo_ros_pkg = get_package_share_directory("gazebo_ros")
    simu_pkg = get_package_share_directory("in424_simu")

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_pkg, "launch", "gazebo.launch.py")
        )
    )
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(simu_pkg, "models")

    spawn_robots_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(simu_pkg, "launch", "spawn_robots_launch.py")
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "world",
            default_value = os.path.join(simu_pkg, "worlds", "env.world"),
            description = "World file to use for the simulation"
        ),

        gazebo_launch,
        spawn_robots_launch,

        Node(
            package = "rviz2",
            executable = "rviz2",
            arguments = ["-d", os.path.join(simu_pkg, "cfg", "config.rviz")]
        )
    ])