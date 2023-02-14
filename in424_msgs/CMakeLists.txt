cmake_minimum_required(VERSION 3.0.2)
project(in424_msgs)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  message_generation
  std_msgs
)

add_service_files(FILES DistToFlag.srv)
generate_messages(DEPENDENCIES geometry_msgs std_msgs)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES in424_msgs
#  CATKIN_DEPENDS geometry_msgs message_generation std_msgs
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)