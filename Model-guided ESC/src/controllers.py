#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import message_filters
from line_laser_ros.msg import CleanData
from line_laser_ros.msg import Costpara
from scipy import signal
import statistics
import numpy as np
import math


class controllers:

    omega = 0.5
    phase = 0
    pred_base = {0:4.7, 1:3.34, 2:2.1, 3:1.56}
    pred1 = []
    Rd = 0.0
    R = 0.0
    lamb = 0.07
    a = 0.2
    delta_t = 0.0
    t_now1 = 0.0
    count_J1 = 0
    count_J2 = 0
    SavefileJ = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/tuneJ.txt", "a+")
    SavefileRd = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/tuneRd.txt", "a+")
    SavefileT = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/ESCtime.txt", "a+")
    SavefileFOV = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/FOV.txt", "a+")
    Savefilecount = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/count.txt", "a+")
    SavefileI = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/intensity.txt", "a+")
    Savefilea = open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/OD2/a.txt","a+")
    def __init__(self):   # _init_ method defines the instantiation operation."self" variablerepresents the instance of the object itself
        self.publisher_Rd = rospy.Publisher("Rd", std_msgs.msg.Float32, queue_size=1)
        self.subscriber_controller = rospy.Subscriber("controller",std_msgs.msg.String,self.callback_controller, queue_size=1)
        self.subscriber_pred = rospy.Subscriber("pred",std_msgs.msg.Int16, self.callback2, queue_size=1)
        self.subscriber_J = rospy.Subscriber("cost",std_msgs.msg.Float32,self.callback_J,queue_size=1)
        self.subscriber_cd=rospy.Subscriber("costpara", Costpara, self.callback,queue_size=1)
	self.t1 = rospy.get_time()
        #self.HPFhis = np.zeros(self.filterorder + 1, dtype=float)
        #self.Yout = np.zeros(self.filterorder + 1, dtype=float)

    def callback(self,costpara):
        self.range = costpara.range
	self.intensity = costpara.intensity
	self.count = costpara.count
	self.FOV = costpara.FOV

    def callback2(self,pred):
        self.pred = pred.data

    def callback_J(self,cost):
        self.J = cost.data
        if self.J < 30:#20:
	    self.count_J1 = self.count_J1 + 1
	    self.count_J2 = 0
	elif self.J > 40:
	    self.count_J2 =self.count_J2 + 1
	    self.count_J1 = 0

    def ESC(self):
        t_now0 = rospy.get_time()
	if self.count_J2 >=5:#3:
	    self.a = 0.2    
	    self.delta_t = 0
	if self.count_J1 >=3:
	    self.a = 0.2* math.exp(-self.lamb * self.delta_t)
	if self.a < 0.01:
	    self.a = 0.01
        dr = self.J * self.a * math.sin(self.omega * t_now0) #omega = 0.5,sin A 0.2
        K = 0.1 #0.1
        self.R = self.R - dr * 0.1 * K
        self.Rd = self.R + self.a * math.sin(self.omega * t_now0) #omega = 0.5
	self.delta_t = self.delta_t + 0.5
	print ("a:",self.a)
	print(self.Rd)
	print("Lidar",self.range)
	print("J:",self.J)
	self.SavefileFOV.write(str(self.FOV)+"\n")
	self.Savefilecount.write(str(self.count)+"\n")
	self.SavefileI.write(str(self.intensity)+"\n")
	self.SavefileJ.write(str(self.J)+"\n")
	self.SavefileRd.write(str(self.Rd)+"\n")
	#self.SavefileLR.write(str(self.range)+"\n")
	self.SavefileT.write(str(t_now0)+"\n")
	self.Savefilea.write(str(self.a)+"\n")
        return self.Rd

    def Lookup(self):
        while len(self.pred1) < 7:
            self.pred1.append(self.pred)
        pred_most = statistics.mode(self.pred1)
        print("Lookup")
        self.Rd = self.pred_base[pred_most]
        del self.pred1[:]
        return self.Rd

    def callback_controller(self,controller):
        if controller.data == "Lookup":
            self.Lookup()
        elif controller.data == "ESC_Re":
            self.R = self.range
	    self.delta_t = 0
	    self.t1 = rospy.get_time()
            print("Reset")
            self.ESC()
        else:
            self.ESC()
        self.publisher_Rd.publish(self.Rd)

if __name__ == '__main__':
    rospy.init_node('pred')
    controllers = controllers()
    
    try:
        rospy.spin()
    except:
        print("sth wrong")


#def ESC(self):
#        for k in range(1, self.filterorder + 1):
#            self.Yout[k - 1] = self.Yout[k]
#            self.HPFhis[k - 1] = self.HPFhis[k]
#        self.Yout[self.filterorder] = self.J
#        HPFnew = 0
#        for j in range(1, self.filterorder + 2):
#            HPFnew = HPFnew + self.b[j - 1] * self.Yout[self.filterorder + 1 - j]
#        for j in range(2, self.filterorder + 2):
#            HPFnew = HPFnew - self.a[j - 1] * self.HPFhis[self.filterorder + 1 - j]
#        self.HPFhis[self.filterorder] = HPFnew
#        t_now = rospy.get_time() # t_now is timer inside ros
#        dt = rospy.Time(0.1) # set dt as 0.1
#        dr = HPFnew * math.sin(self.omega * t_now + self.phase)
#	print(dr)
#        K = 0.05
#        self.R = self.R + dr * dt.secs * K
#        self.Rd = self.R + math.sin(self.omega * t_now + self.phase)
#        return self.Rd
#filterorder = 2
#   b,a = signal.butter(filterorder, 0.09,'highpass')

#if count<3 and (math.sin(self.omega * t_now) ==1 or -1):
	#    return self.Rd
 	#    count = count+1
#print(self.Rd)
#print("Lidar",self.range)
#print("J:",self.J)
#self.SavefileJ.write(str(self.J)+"\n")
#self.SavefileRd.write(str(self.Rd)+"\n")
#self.SavefileLR.write(str(self.range)+"\n")
