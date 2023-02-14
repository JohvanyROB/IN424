#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Range
from in424_msgs.srv import DistToFlag


class Robot:
    def __init__(self, robot_name, nb_flags):
        self.sonar = 0.0 #Sonar distance
        self.robot_name = robot_name
        self.ns = "/" + self.robot_name
        self.nb_flags = nb_flags    #Number of flags to discover in the environment

        rospy.wait_for_service('/dist_to_flag')
        self.dtf_srv = rospy.ServiceProxy('/dist_to_flag', DistToFlag)

        '''Listener and publisher'''
        rospy.Subscriber(self.ns + "/sensor/us_front", Range, self.sonar_cb)
        self.cmd_vel_pub = rospy.Publisher(self.ns + "/cmd_vel", Twist, queue_size=1)


    def sonar_cb(self, msg):
        #DO NOT TOUCH
        self.sonar = msg.range

    
    def constrain(self, val, min=-2.0, max=2.0):
        #DO NOT TOUCH
        if val < min: return min
        if val > max: return max
        return val


    def set_speed_angle(self, linear_vel, angular_vel):
        #DO NOT TOUCH
        cmd_vel = Twist()
        cmd_vel.linear.x = self.constrain(linear_vel)
        cmd_vel.angular.z = self.constrain(angular_vel, min=-1, max=1)
        self.cmd_vel_pub.publish(cmd_vel)

    
    def getDistanceToFlag(self):
        try:
            pose = Vector3()
            pose.x = 0.0
            pose.y = 0.0
            result = self.dtf_srv(pose)
            return (result.id_flag, result.distance)
        except rospy.ServiceException as e :
            print(f"Service call failed: {e}")


    def euler_from_quaternion(self, x, y, z, w):
        #DO NOT TOUCH
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = 2.0 * (w * x + y * z)
        t1 = 1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = self.constrain(2.0 * (w * y - z * x), -1, 1)
        pitch_y = math.asin(t2)

        t3 = 2.0 * (w * z + x * y)
        t4 = 1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z # in radians    



if __name__ == "__main__":
    print("Running ROS..")
    rospy.init_node("Strategy", anonymous=True)

    try:
        robot_name = rospy.get_param("~robot_name")
        nb_flags = rospy.get_param("nb_flags")
        robot = Robot(robot_name, nb_flags)
        print(f"Robot {robot_name} is starting")

        while not rospy.is_shutdown():
            # WRITE YOUR STRATEGY HERE...
            linear_velocity = 0
            angular_velocity = 0
            print(f"SONAR VALUE : {robot.sonar:.2f}")
            print(f"Distance to flag : {robot.getDistanceToFlag()}")



            #Finishing by publishing the desired speed.
            robot.set_speed_angle(linear_velocity, angular_velocity)
            rospy.sleep(0.5)    #pause the while loop for 0.5 second (considering the simulation time!!!)

    except rospy.exceptions.ROSInterruptException:
        pass