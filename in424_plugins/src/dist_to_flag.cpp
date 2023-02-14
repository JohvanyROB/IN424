#include <in424_plugins/dist_to_flag.hpp>

namespace gazebo{
    DistanceToFlagPlugin::DistanceToFlagPlugin(): distribution_(0, 0.05){
    }


    DistanceToFlagPlugin::~DistanceToFlagPlugin(){
        nh_->shutdown();
        delete nh_;
    }


    void DistanceToFlagPlugin::Load(physics::WorldPtr world, sdf::ElementPtr sdf){
        int nb_flags = 0;
        if(sdf->HasElement("nb_flags"))
            nb_flags = sdf->GetElement("nb_flags")->Get<int>();

        //Get the flags poses and store them in the list flags_poses_
        for(int i = 1; i < nb_flags+1; i++){
            ignition::math::Pose3d model_pose = world->ModelByName("flag_" + std::to_string(i))->WorldPose();
            geometry_msgs::Vector3 flag_pose;
            flag_pose.x = model_pose.Pos().X();
            flag_pose.y = model_pose.Pos().Y();
            flags_poses_.push_back(flag_pose);
        }

        nh_ = new ros::NodeHandle();
        dtf_service_ = nh_->advertiseService("dist_to_flag", &DistanceToFlagPlugin::distance_to_flag_srv, this);
        nh_->setParam("nb_flags", nb_flags);
    }


    float DistanceToFlagPlugin::getMinDist(const geometry_msgs::Vector3& msg, int* imin){
        float min_dist = FLT_MAX;
        float dx, dy, dist;
        for(int i = 0; i < flags_poses_.size(); i++){
            dx = flags_poses_[i].x - msg.x;
            dy = flags_poses_[i].y - msg.y;
            dist = std::sqrt(dx*dx + dy*dy);
            if(dist < min_dist){
                min_dist = dist;
                *imin = i+1; //the flag id starts at 1 not 0 (their gazebo model name)
            }
        }
        return min_dist;
    }


    bool DistanceToFlagPlugin::distance_to_flag_srv(in424_msgs::DistToFlag::Request& req, in424_msgs::DistToFlag::Response& res){
        int imin = 1;
        res.distance = getMinDist(req.coords, &imin) + distribution_(generator_);
        res.id_flag = imin;
        return true;
    }

    GZ_REGISTER_WORLD_PLUGIN(DistanceToFlagPlugin)
}