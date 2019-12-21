#!/usr/bin/env python

import tf
import roslib
import rospy
import std_msgs.msg
from geometry_msgs.msg import Twist
import message_filters
from line_laser_ros.msg import CleanData
from line_laser_ros.msg import Costpara
from scipy import signal
from sensor_msgs.msg import Imu
import math


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

class MobileTwist:
    
    speed = 1
    turn = 1.0
    twist = Twist()
    k = 0.2
    delta_R = 0
    heading = 0.0
    pred_base = {0:4.5, 1:2.6, 2:2.1, 3:1.98}
    flag_initial = 0
    err = 0.0
    err_last = 0.0
    count_J1 = 0
    count_J2 = 0
    ## datasaving
    SavefilespeedX = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/speedX.txt", "a+")
    SavefilespeedY = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/speedY.txt", "a+")
    SavefileRd = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/Rd.txt", "a+")
    SavefileLR = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/LR.txt", "a+")
    SavefileT = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/time.txt", "a+")
    SavefilePred = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/pred.txt", "a+")

    def __init__(self):   
        self.pub_twist = rospy.Publisher('cmd_vel',Twist,queue_size=1)
        self.subscriber_data = rospy.Subscriber("costpara", Costpara, self.callback1,queue_size=1) #targeted performances; arguments in J
        self.subscriber_pred = rospy.Subscriber("pred",std_msgs.msg.Int16, self.callback2, queue_size=1) #EI 
	self.subscriber_Rd = rospy.Subscriber("Rd", std_msgs.msg.Float32, self.callback_Rd, queue_size=1) #command optimal range
	self.subscriber_J = rospy.Subscriber("cost",std_msgs.msg.Float32,self.callback_J,queue_size=1) 
        self.publisher_ctl = rospy.Publisher("controller",std_msgs.msg.String,queue_size=1) 
	self.subscriber_imu = rospy.Subscriber("imu/data",Imu,self.callback_imu,queue_size = 1)

    def callback1(self,costpara):
        self.intensity = costpara.intensity
        self.range = costpara.range

###counter for cost to judge the cost condition
    def callback_J(self,cost):
        self.J = cost.data
	if self.flag_initial ==1:
	    if self.J <30:# 20:
	        self.count_J1 = self.count_J1 + 1
		self.count_J2 = 0
	    elif self.J > 40:
	        self.count_J2 =self.count_J2 + 1
		self.count_J1 = 0
	    if self.count_J1 >=3:
		self.twist.linear.y = 0#-0.15
	    elif self.count_J2 >=3:
		self.twist.linear.y = 0

###flags for different controller to choose the different execution
 
    def callback2(self,pred):
        self.pred = pred.data
	self.SavefilePred.write(str(self.pred)+"\n")
        error_r = self.pred_base[self.pred] - self.range
        if (self.flag_initial == 0):# or (abs(error_r)>= 2):
            self.publisher_ctl.publish("Lookup")
            self.flag_initial = 0

        elif (self.flag_initial == 2):
            self.publisher_ctl.publish("ESC_Re")
            self.flag_initial = 1

        else:
            self.publisher_ctl.publish("ESC")
            self.flag_initial = 1

    def callback_imu(self,imu_msg):
        quaternion = (
            imu_msg.orientation.x,
            imu_msg.orientation.y,
            imu_msg.orientation.z,
            imu_msg.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)

        self.heading = euler[2]


    def callback_Rd(self, Rd):
        self.Rd = Rd.data
	self.err_last = self.err
	self.err = self.range - self.Rd
	if abs(self.err)<=0.01:
	    self.twist.linear.x = 0
	self.sum = 0.15*self.err + 0.15*(self.err_last +self.err) + 0.2*(self.err - self.err_last)#-0.25,0.15
        if self.range > 4.8:
            #self.Rd = 4
            self.twist.linear.x = 0.2; self.twist.linear.y = 0
        elif self.range < 0.7:
            #self.Rd = 2
            self.twist.linear.x = -0.3; self.twist.linear.y = 0
	elif self.flag_initial== 0:   #beginning period
            if abs(self.err) <= 0.4 : #gaurantee initial esc start point closer
                self.twist.linear.x = 0.0; self.twist.linear.y = 0
		self.flag_initial = 2
	    else:
               if abs(self.sum) < 0.4:
	          self.twist.linear.x = self.sum
	       elif abs(self.sum) < 0.8:
                     self.twist.linear.x = self.sum * self.speed *0.5
               else: 
                     self.twist.linear.x = self.sum * self.speed *0.1

        else:
	    if self.Rd <= 0:
		self.twist.linear.x = 0; self.twist.linear.y = 0
		
	    elif abs(self.Rd)<6:
		if abs(self.sum) < 0.01:
		    self.twist.linear.x = 0
		elif abs(self.sum) < 0.15:
		    self.twist.linear.x = self.sum * self.speed * 2
		elif abs(self.sum) < 0.4:
		    self.twist.linear.x = self.sum * self.speed
		elif abs(self.sum) < 0.8:
		     self.twist.linear.x = self.sum * self.speed *0.5
		elif abs(self.sum) < 1.2:
		     self.twist.linear.x = self.sum * self.speed *0.2   
	    else: 
                self.twist.linear.x = 0
		self.flag_initial = 0
        self.twist.linear.z = 0; self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = -1*math.sin(self.heading*0.5)
	print("speed:",self.twist.linear.x)
	#print("error:",self.err)
	self.SavefileRd.write(str(self.Rd)+"\n")
	self.SavefileLR.write(str(self.range)+"\n")
	self.SavefileT.write(str(rospy.get_time())+"\n")
	self.SavefilespeedX.write(str(self.twist.linear.x)+"\n")
	self.SavefilespeedY.write(str(self.twist.linear.y)+"\n")
        #iself.pub_twist.publish(self.twist)
        #r.sleep()

   
if __name__=="__main__": 
    rospy.init_node('twist')
    r = rospy.Rate(3)
    mobiletwist = MobileTwist()
    #try:
    while not rospy.is_shutdown():
	mobiletwist.pub_twist.publish(mobiletwist.twist)
        r.sleep()
    rospy.spin()
    #except:
     #   print("sth wrong")
