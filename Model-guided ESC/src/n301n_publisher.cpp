#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <boost/asio.hpp>
#include <std_msgs/UInt16.h>
#include <n301n_lidar.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "line_laser");
    ros::NodeHandle nh;
    ros::NodeHandle priv_nh("~");

    std::string port;
    int baud_rate;
    int version_num;
    std::string frame_id;

    std_msgs::UInt16 rpms;

    priv_nh.param("port", port, std::string("/dev/ttyUSB0"));
    priv_nh.param("baud_rate", baud_rate, 115200);
    priv_nh.param("frame_id", frame_id, std::string("laser_link"));
    priv_nh.param("version_num", version_num, 1);   // 1 is line laser; 2 is line laser (0.5deg); 0 is n301(360)


    boost::asio::io_service io;
    try{
        n301_lidar_driver::n301n_lidar laser(port, baud_rate, io);
        ros::Publisher laser_pub = nh.advertise<sensor_msgs::LaserScan>("scan", 1000);
        ros::Publisher motor_pub = nh.advertise<std_msgs::UInt16>("rpms", 1000);

        switch (version_num)
        {
        case 0:
            ROS_INFO("It is n301 TOF with 360 deg FOV");
            break;
        case 1:
            ROS_INFO("It is line laser with 1 deg resolution");
            break;
        case 2:
            ROS_INFO("It is line laser with 0.5 deg resolution");
            break;
        default:
            ROS_INFO("It is default setting that line laser with 1 deg resolution");
        }

        while(ros::ok()){
            sensor_msgs::LaserScan::Ptr scan(new sensor_msgs::LaserScan);
            if(scan == NULL)
                ROS_INFO("SCAN == NULL");
            scan->header.frame_id = frame_id;
            scan->header.stamp = ros::Time::now();
            laser.poll(scan, version_num);
            rpms.data = laser.rpms;
            laser_pub.publish(scan);
            motor_pub.publish(rpms);
        }
        laser.close();
        return 0;
    }
    catch (boost::system::system_error ex){
        ROS_ERROR("Error instantiating laser object. Are you sure you have the correct port and baud rate? Error was %s", ex.what());
        return -1;
    }
}
