#!/usr/bin/env python

import rospy
from line_laser_ros.msg import CleanData
from line_laser_ros.msg import Costpara
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import pickle
import std_msgs.msg
from collections import Counter
import statistics

scaler=joblib.load("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/model/scal_b1s4c.model")
clf=joblib.load("/home/nvidia/Desktop/catkin_ws/src/robot_formation/LS02A/model/clf_b1s4c.model")
#with open('/home/xchen/catkin_ws/src/LS02A/data/scal1.txt','r') as f1:
#    scaler2=pickle.load(f1)
#with open('/home/xchen/catkin_ws/src/LS02A/data/dataFile1.txt','r') as f2:
#    clf2=pickle.load(f2) 

class Pred_Cost:

    r=[]
    i=[]
    b=[]
    c=[]
    J=[]

    def __init__(self):
        self.subscriber_cd = rospy.Subscriber("costpara",Costpara, self.callback,queue_size=1)
        self.publisher_pred = rospy.Publisher('pred',std_msgs.msg.Int16,queue_size=1)
	self.publisher_cost = rospy.Publisher('cost',std_msgs.msg.Float32,queue_size=1)

    def callback(self,costpara):
        self.J.append((0.5*(costpara.intensity/10-40)**2) + (0.4*(costpara.count-20)**2 - 0.1*10*costpara.FOV))#ori *10
        #self.publisher_cost.publish(J)
        self.r.append(costpara.range)
        self.i.append(costpara.intensity)
        self.c.append(costpara.count)
        self.b.append(costpara.range*costpara.range*costpara.intensity)
        while len(self.r) == 3:
            data_temp = np.column_stack((self.r,self.i,self.b,self.c))
	   # pred = clf.predict(scaler.transform(data_temp))
            pred = Counter(clf.predict(scaler.transform(data_temp))).most_common(1)[0][0]
            self.publisher_pred.publish(pred)
	    self.publisher_cost.publish(statistics.median(self.J))
        #self.Savefile.write(str(pred)+"\n")
            del self.r[:],self.i[:],self.b[:],self.c[:],self.J[:]
     
if __name__ == '__main__':
    rospy.init_node('pred')
    Pred_Cost=Pred_Cost()
   # rate=rospy.Rate(0.1)
    try:
        rospy.spin()
    except:
        print("sth wrong")
   #     rate.sleep()
