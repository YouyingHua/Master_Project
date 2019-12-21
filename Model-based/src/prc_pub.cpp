#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include "sensor_msgs/LaserScan.h"
#include <vector>
#include <fstream>
#include <line_laser_ros/CleanData.h>
#include <std_msgs/Header.h>
#include <stdio.h>
//class LaserFilter
//    public:
//   ros::Subscriber sub = ns.subscribe("scan", 100, subCallback);
    //ros::Publisher pub = ns.advertise<std_msgs::String>("laserfilter", 100);
// struct Data_new{   //struct name
//     std::vector<float> ranges;
//     std::vector<float> intensities
// };

// Data_new data_new;  //struct obj

// std::vector<Data_new> data_new_vec;//newrange, newintensities;
std_msgs::Header header;
std::vector<float> ranges, intensities, newRange, newIntesity;
line_laser_ros::CleanData cleandata;
//std::vector<line_laser_ros::CleanData> cleandata;//previous:direct define line_laser_ros::XX cleandata
ros::Publisher pub,pub_count;
std_msgs::Int32 count;
//void CleanData(std_msgs::Header header,std::vector<float> ranges,std::vector<float> intensities){
//    for (int i=0; i<=ranges.size();i++){
//        if ((intensities[i]<101)||(intensities[i]>1499))
//            continue;
//        else 
//            cleandata.header=header;
//            cleandata.range=ranges[i];
//            cleandata.intensity=intensities[i];
//            beta=ranges[i]*intensities[i]*intensities[i];
//            cleandata.beta=beta;
//        cleandata = cleandata;
//        pub.publish(cleandata);
//           }  
//}
void subCallback(const sensor_msgs::LaserScan::ConstPtr data){
        
        ranges=data -> ranges;
        intensities=data -> intensities;
        header=data -> header;
        std::ofstream ftest("/home/xchen/catkin_ws/src/LS02A/data/test.txt",std::ios::app);
        //std::vector<float>::const_iterator first = ranges.begin() +30;
        //std::vector<float>::const_iterator last = ranges.begin() +60;
        newRange.resize(20);
        newIntesity.resize(20);
        memcpy(&newRange[0],&ranges[34],20*sizeof(uint32_t));
        memcpy(&newIntesity[0],&intensities[34],20*sizeof(uint32_t));
        count.data = 0;
        for (int i = 0; i<=newRange.size()-1;i++){
			if((newIntesity[i]==0)||newRange[i]==0){
				continue;}
            //else if((newIntesity[i]<0.1)||(newIntesity[i]>10000)){//if ((newRange[i]!=newRange[i])||(newRange[i]<0.1))
             //   std::cout<< i <<std::endl;
              //  cleandata.range=0;
               // cleandata.intensity=0;}
            else{
                count.data++;
                cleandata.range=newRange[i];
                cleandata.intensity=newIntesity[i];}

            cleandata.beta=cleandata.range * cleandata.range * cleandata.intensity;
            pub.publish(cleandata);}
        //std::cout << count.data << std::endl;
        pub_count.publish(count);
		//if(count>0){
        //ftest << count << std::endl;}
        
}
            
int main(int argc, char *argv[]){
    ros::init(argc, argv, "prc_pub");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("scan", 1, subCallback);
    pub=nh.advertise<line_laser_ros::CleanData>("cleandata",50);
    pub_count = nh.advertise<std_msgs::Int32>("count", 10);

    ros::spin();
    }
