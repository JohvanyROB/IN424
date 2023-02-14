#ifndef DISTANCE_TO_FLAG_HPP
#define DISTANCE_TO_FLAG_HPP

//Gazebo
#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

//ROS
#include <ros/ros.h>
#include <geometry_msgs/Vector3.h>
#include <in424_msgs/DistToFlag.h>

//Other
#include <random>


namespace gazebo{
    class DistanceToFlagPlugin: public WorldPlugin{
        public:
            DistanceToFlagPlugin();
            virtual ~DistanceToFlagPlugin();

        protected:
            virtual void Load(physics::WorldPtr world, sdf::ElementPtr sdf);
        
        private:
            ros::NodeHandle* nh_;
            ros::ServiceServer dtf_service_;
            std::default_random_engine generator_;
            std::normal_distribution<double> distribution_;
            std::vector<geometry_msgs::Vector3> flags_poses_;

            float getMinDist(const geometry_msgs::Vector3& msg, int* imin);
            bool distance_to_flag_srv(in424_msgs::DistToFlag::Request& req, in424_msgs::DistToFlag::Response& res);
    };
}

#endif