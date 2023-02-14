#Setup your sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

#Set up your keys
sudo apt update && sudo apt install curl -y # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

#Installation
sudo apt update && sudo apt install ros-noetic-desktop-full -y

#Dependencies for building packages
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y
sudo rosdep init
rosdep update

#Create a ROS workspace
mkdir -p ~/catkin_ws/src
source /opt/ros/noetic/setup.bash
cd ~/catkin_ws && catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc