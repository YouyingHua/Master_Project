#include "ros/ros.h"
#include "std_msgs/String.h"
#include <stdint.h>
#include <iostream>
#include <sys/types.h>
#include "sensor_msgs/LaserScan.h"
#include "std_msgs/Header.h"
#include <vector>
#include <fstream>
#include <line_laser_ros/CleanData.h>

std::vector<float> ranges, intensities;//newrange, newintensities;
line_laser_ros::CleanData cleandata;
uint32_t seq;
// void Savefile(float range, float intensity){ //void Savefile(uint32_t seq, std::vector<float> ranges,std::vector<float> intensities)
//     std::ofstream fout("/home/xchen/catkin_ws/src/LS02A/data/OD0.txt",std::ios::app);
//     if (fout){
//     for (int i=0; i<=ranges.size();i++){
//         fout<<ranges[i]<<"  "<<intensities[i]<<std::endl; //fout<<seq<<" "<< ranges[i]<<"  "<<intensities[i]<<std::endl;
//         std::cout<<ranges[i]<<"  "<<intensities[i]<<std::endl; //std::cout<<seq<<" "<<ranges[i]<<"  "<<intensities[i]<<std::endl
//         }
//     fout.close();}
//     else 
//     std::cout<<"fout error!"<<std::endl;
// }

void Savefile(float range, float intensity, float beta){
    std::ofstream fout("/home/xchen/catkin_ws/src/LS02A/data/OD02.txt",std::ios::app);
     if (fout){
         fout<<range<<"  "<<intensity<<" "<<beta<<std::endl; }
        // std::cout<<range<<"  "<<intensity<<std::endl;} 
     else 
        std::cout<<"fout error!"<<std::endl;
     
}

void subCallback(line_laser_ros::CleanData cleandata){
        //ranges=data -> ranges;
        //intensities=data -> intensities;
        //seq=data -> header.seq;
        
        Savefile(cleandata.range,cleandata.intensity,cleandata.beta);// add seq
        std::cout<<"saving"<<std::endl;
        //std::cout<<"fout error"<<std::endl;
}
    
int main(int argc, char *argv[])
{
    ros::init(argc, argv, "laserfilter");
    ros::NodeHandle ns;
    ros::Subscriber sub = ns.subscribe("cleandata", 100, subCallback);//try scan or scan_filtered next step as scan-type
    ros::spin();
    }