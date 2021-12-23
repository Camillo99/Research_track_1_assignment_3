#! /usr/bin/env python

import rospy
import numpy
from geometry_msgs.msg import Twist, Vector3    #for cmd_vel topic
from sensor_msgs.msg import LaserScan           #for scan topic

#linit distance to an ovstacle for avoiding collision
min_star = 0.5

#initialize a Twist object for the publisher
init = Vector3(0, 0, 0)
repost = Twist( init, init)


def compute_min_dist(ranges):
    #first block -> right side
    #second block -> front side
    #third block -> left side
    #init
    distance = [0,0,0]
    #divide the ranges array in 3 parts
    #right part
    #middle part
    #left part
    sub_right = ranges[0:240]
    sub_mid = ranges[240:480]
    sub_left = ranges[480:721]
    #compute and store the min distance
    distance[0] = min(sub_right)
    distance[1] = min(sub_mid)
    distance[2] = min(sub_left)
    return distance
        
  

def callback_scan(data):
    #use a global variable 
    global repost
    #initialize the publisher
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    #compute the minimun obsable distance to the right, left and in front of the robot
    distances = compute_min_dist(data.ranges)

    if distances[0] < min_star :
        if repost.angular.z < 0 :
            #avoid turning right -> w = -1   
            repost.angular.z = 0    
    if distances[1] < min_star:
        if repost.linear.x > 0 :
            #deny moving toward an obstacle
            repost.linear.x = 0
    if distances[2] < min_star :
        if repost.angular.z > 0 :
            #avoid turning left -> w = 1
            repost.angular.z = 0
    #pubblic on topic cmd_vel to the robot
    pub.publish(repost)




#copy remap_cmd_vel on repost -> ready to be:
#modified by the controller or
#reposted as it was
def callback_remap(data):
    #use a global variable
    global repost
    repost = data
  
def keyboard_remap():
    #initialize the node
    rospy.init_node('keyboard_remap_node')
    #subscriber to topic remap_cmd_vel    
    rospy.Subscriber("/remap_cmd_vel", Twist, callback_remap)
    #subscriber to topic scan
    rospy.Subscriber("/scan", LaserScan, callback_scan)
    rospy.spin()
    
#main 
if __name__=="__main__":
    keyboard_remap()
