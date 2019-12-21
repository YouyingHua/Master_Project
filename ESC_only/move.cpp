#include <geometry_msgs/Twist.h>
#include "ros/ros.h"
#include <stdio.h>
geometry_msgs::Twist msg;
int main(int argc, char *argv[])
{
    ros::init(argc, argv, "move");
	ros::NodeHandle nm;
	ros::Publisher pub_cmd = nm.advertise<geometry_msgs::Twist>("cmd_vel",1000);
	while(ros::ok()){
		msg.linear.x = -0.1; msg.linear.y = -0.1; msg.linear.z = 0; msg.angular.x = 0; msg.angular.y = 0; msg.angular.z = 0;
		//std::cout<<msg<<std::endl;
		pub_cmd.publish(msg);}
	
    ros::spin();}