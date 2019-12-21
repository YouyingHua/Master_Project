#!/usr/bin/env python

import rospy
from line_laser_ros.msg import CleanData
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
#from sklearn.neural_network import MLPClassifier
import pickle
import statistics
import std_msgs.msg

scaler=joblib.load("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/scal0.model")
clf=joblib.load("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/clf0.model")
#with open('/home/xchen/catkin_ws/src/LS02A/data/scal1.txt','r') as f1:
#    scaler2=pickle.load(f1)
#with open('/home/xchen/catkin_ws/src/LS02A/data/dataFile1.txt','r') as f2:
#    clf2=pickle.load(f2) 
f=open("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/data/pred.txt", "a+")

class Pred:

    r=[]
    i=[]
    b=[]

    def __init__(self):
        self.subscriber_cd=rospy.Subscriber("cleandata",CleanData, self.callback,queue_size=1)
        self.publisher_pred=rospy.Publisher('pred',std_msgs.msg.Int16,queue_size=1)

    def callback(self,cleandata):
        while len(self.r)<=100:
            self.r.append(cleandata.range)
            self.i.append(cleandata.intensity)
            self.b.append(cleandata.beta)
        data=np.column_stack((self.r,self.i,self.b))
        #if len(data)>=20: #change add this if
        pred=statistics.mode(clf.predict(data))
        self.publisher_pred.publish(pred)
	print(pred)
	f.write('%s\n'%pred)
        del self.r[:],self.i[:],self.b[:]


            #self.subscriber_cd.unregister() 
     
if __name__ == '__main__':
    rospy.init_node('pred')
    Pred=Pred()
   # rate=rospy.Rate(0.1)
    try:
        rospy.spin()
    except:
        print("sth wrong")
   #     rate.sleep()
