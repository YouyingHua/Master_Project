#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
from geometry_msgs.msg import Twist
import message_filters
from line_laser_ros.msg import CleanData

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

class MobileTwist:
    
    pred_base = {0:4.5, 1:4.5, 2:4, 3:4, 4:2.574, 5:2.339, 6:1.98} #dict([(0,6,13,19),(4,3,2,1)])
    speed = 1
    turn = 1.0
    twist = Twist()
    
    def __init__(self):   # _init_ method defines the instantiation operation."self" variablerepresents the instance of the object itself
        self.pub_twist = rospy.Publisher('cmd_vel',Twist,queue_size=1)
        self.subscriber_data = rospy.Subscriber("cleandata", CleanData, self.callback1,queue_size=1)
        self.subscriber_pred = rospy.Subscriber("pred",std_msgs.msg.Int16, self.callback2, queue_size=1)
        self.subscriber_count = rospy.Subscriber("count",std_msgs.msg.Int32,self.callback3,queue_size=1)

    def callback3(self,count):
        self.count = count

    def callback1(self,cleandata):
        self.intensity = cleandata.intensity
        self.range = cleandata.range

    def callback2(self,pred):
    # fix intensity way:
        #  r = rospy.Rate(10)
        #  while pred.data in self.pred_base:
        #      if self.pred_base[pred.data] > self.intensity:
        #          x = 1
        #      elif self.pred_base[pred.data] <= self.intensity:
        #          x = -1
        #      self.twist.linear.x = x*self.speed; self.twist.linear.y = -0.1; self.twist.linear.z = 0
        #      self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0
        #      if not(self.range < 0.5 or self.range > 4.5):
        #          pass
        #      else:
        #          self.twist.linear.x = 0
        #          rospy.loginfo("out of detection area!")

        #      self.pub_twist.publish(self.twist)
        #      r.sleep()
        #optimal range way:
        r = rospy.Rate(10)
        while pred.data in self.pred_base:
            if self.count.data > 15:
                print(self.count.data)
                if self.pred_base[pred.data] > self.range:
                    x = -1 #-1
                elif self.pred_base[pred.data] <= self.range:
                    x = 1
            else:
                x = 1
                
            self.twist.linear.x = x*self.speed; self.twist.linear.y = -0.2; self.twist.linear.z = 0
            self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

            self.pub_twist.publish(self.twist)
            r.sleep()
        
if __name__=="__main__":
    #mobiletwist = MobileTwist() 
    rospy.init_node('twist')
    #r = rospy.Rate(10)
    mobiletwist = MobileTwist()
    try:
        #mobiletwist.pub_twist.publish(mobiletwist.twist)
        #r.sleep()
        rospy.spin()
    except:
        print("sth wrong")
