cmake_minimum_required(VERSION 3.0.2)
project(in424_plugins)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  geometry_msgs
  roscpp
  in424_msgs
)

find_package(gazebo REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES in424_plugins
#  CATKIN_DEPENDS gazebo_ros geometry_msgs roscpp
#  DEPENDS system_lib
)

link_directories(${GAZEBO_LIBRARY_DIRS})

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")

add_library(dist_to_flag src/dist_to_flag.cpp)
target_link_libraries(dist_to_flag ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})