#!/bin/bash

sudo apt update -y

# Install project's dependencies 
sudo apt -y install python3-colcon-common-extensions
sudo apt -y install python3-pip
sudo apt -y install ros-galactic-gazebo-ros-pkgs ros-galactic-tf-transformations ros-galactic-tf2-tools ros-galactic-teleop-twist-keyboard ros-galactic-xacro

pip3 install transforms3d


echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc
source /opt/ros/galactic/setup.bash
cd ~/ros2_ws && colcon build --symlink-install
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc