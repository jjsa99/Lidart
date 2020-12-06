#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int8
from std_msgs.msg import String, Float32MultiArray
from geometry_msgs.msg import Pose

pub1 = 0
# pub2 = 0
# pub3 = 0
pub4 = 0
pub5 = 0

def send2Mirror():
    
    global pub1
    # global pub2
    # global pub3
    global pub4
    global pub5
    
    while(1):
        i = input("\n1 - [FOV_horizontal FOV_vertical STEP_horizontal STEP_vertical]\n2 - Next Position\n3 - STOP\n4 - QUIT\n\nSelect an operation:")
        if(i == '1'):
            FOVh = 30
            FOVv = 30
            steph = 5
            stephv = 5
            print("value 1")
            
            param = Float32MultiArray()
            # param.data = [FoVh,FoVv,steph,stepv]
            param.data = [30,30,5,5]
            pub1.publish(param)
            
        #if(i=='2'):
            #pub2.publish(1)
            # pub3.publish(1)
            
        if(i=='3'):
            pub4.publish(1)
            
        if(i=='4'):
            pub5.publish(1)
            break
    print("out cycle")
        

def testMirror():
	
    global pub1
    # global pub2
    # global pub3
    global pub4
    global pub5

    rospy.init_node('testMirror', anonymous=True)
    
    pub1 = rospy.Publisher('Mirror_Pattern', Float32MultiArray, queue_size=10)
    # pub2 = rospy.Publisher('Photo1', Int8, queue_size=10)
    # pub3 = rospy.Publisher('Photo2', Int8, queue_size=10)
    pub4 = rospy.Publisher('Stop', Int8, queue_size=10)
    pub5 = rospy.Publisher('Quit', Int8, queue_size=10)
    
    send2Mirror()
    # rospy.spin()

if __name__ == '__main__':
    try:
        testMirror()
    except rospy.ROSInterruptException:
        pass
