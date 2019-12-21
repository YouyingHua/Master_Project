#!/usr/bin/env python

import rospy
from line_laser_ros.msg import CleanData
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import pickle
import statistics
import std_msgs.msg

#scaler=joblib.load("/home/xchen/catkin_ws/src/LS02A/model/scal2.model")
clf=joblib.load("/home/xchen/catkin_ws/src/LS02A/model/dataFile2.model")
#with open('/home/xchen/catkin_ws/src/LS02A/model/scal1.txt','r') as f1:
#    scaler2=pickle.load(f1)
#with open('/home/xchen/catkin_ws/src/LS02A/model/dataFile1.txt','r') as f2:
#    clf2=pickle.load(f2) 

class Pred:

    r=[]
    i=[]
    beta=[]
    #data=np.zeros([100,3],floa
    def __init__(self):
        self.subscriber_cd=rospy.Subscriber("cleandata",CleanData, self.callback,queue_size=1)
        self.publisher_pred=rospy.Publisher('pred',std_msgs.msg.Int16,queue_size=1)

    def callback(self,cleandata):
        while len(self.r)<=300:
            self.r.append(cleandata.range)
            self.i.append(cleandata.intensity)
            self.beta.append(cleandata.beta)
        data=np.column_stack((self.r,self.i,self.beta))
 #       data=scaler.transform(data)
        pred=statistics.mode(clf.predict(data))
        #print(pred)
        self.publisher_pred.publish(pred)
        del self.r[:],self.i[:],self.beta[:]

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
