#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include "sensor_msgs/LaserScan.h"
#include <vector>
#include <fstream>
#include <line_laser_ros/CleanData.h>
#include <line_laser_ros/Costpara.h>
#include <std_msgs/Header.h>
#include <stdio.h>

// std::vector<Data_new> data_new_vec;//newrange, newintensities;
std_msgs::Header header;
std::vector<float> ranges, intensities, newRange, newIntesity;
line_laser_ros::CleanData cleandata;
line_laser_ros::Costpara costpara;
ros::Publisher pub,pub_costpara;

void Savefile1(float range, float intensity, float beta){
    std::ofstream fout("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/cleandata.txt",std::ios::app);
     if (fout){
         fout<<range<<"  "<<intensity<<" "<<beta<<std::endl; }
     else 
        std::cout<<"fout error!"<<std::endl;
     
}

void subCallback(const sensor_msgs::LaserScan::ConstPtr data){
        
        ranges=data -> ranges;
        intensities=data -> intensities;
        header=data -> header;
        //std::ofstream ffov("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD0/fov.txt",std::ios::app);
	//std::ofstream fcount("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD0/count.txt",std::ios::app);
	//std::ofstream fI("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD0/intensity.txt",std::ios::app);
        //std::vector<float>::const_iterator first = ranges.begin() +30;
        //std::vector<float>::const_iterator last = ranges.begin() +60;
        newRange.resize(20);
        newIntesity.resize(20);
        memcpy(&newRange[0],&ranges[34],20*sizeof(uint32_t));
        memcpy(&newIntesity[0],&intensities[34],20*sizeof(uint32_t));
        for (int i = 0; i<newRange.size();i++){
	   if((newIntesity[i]==0)||newRange[i]==0){
				continue;}
            else{
                cleandata.range.push_back(newRange[i]);
                cleandata.intensity.push_back(newIntesity[i]);
                cleandata.beta.push_back(newRange[i]*newRange[i]*newIntesity[i]);}
	}

        while(cleandata.range.size()>0){
        double average_R = std::accumulate(cleandata.range.begin(),cleandata.range.end(),0.0)/cleandata.range.size();
        double average_I = std::accumulate(cleandata.intensity.begin(),cleandata.intensity.end(),0)/cleandata.intensity.size();
        costpara.range = average_R;
        costpara.intensity = average_I;
        costpara.count = cleandata.range.size();
        costpara.FOV = average_R*average_R*costpara.count*3.14/360;
	//ffov<< costpara.FOV <<std::endl;
	//fcount<<costpara.count<<std::endl;
	//fI<<costpara.intensity<<std::endl;
        pub.publish(cleandata);
        pub_costpara.publish(costpara);
        cleandata.range.clear();
        cleandata.intensity.clear();
        cleandata.beta.clear();}
}
            
int main(int argc, char *argv[]){
    ros::init(argc, argv, "prc_pub");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("scan", 1, subCallback);
    pub=nh.advertise<line_laser_ros::CleanData>("cleandata",10);
    pub_costpara = nh.advertise<line_laser_ros::Costpara>("costpara", 10);
    
    ros::spin();
    }
