#!/usr/bin/env python

""" ur5_calib.py
    Script used to moving the robot to calibrate wrt to realsense camera.
    This assumes that we have already launched the ur5 bringup node
    author: Michael Andres Lin (michaelv03@gmail.com)
    date: 10/31/2019
"""

import os
import sys
import time
import rospy
import numpy as np
import copy
from std_msgs.msg import String, Int16
from futek_data_logger.msg import z_pos


from ur5_interface import UR5Interface
#from robotiq_interface import RobotiqInterface

# Callback functions    
def state_callback(data):
    incomingString = str(data.data)
    global state, move_completed
#    print("Incoming command: " + incomingString)

    if (incomingString == "home"):
        state = HOME
        move_completed = 0
        
    elif (incomingString == "start"):
        state = START
        move_completed = 0
        
    elif (incomingString == "displace_1"):
        state = DISPLACE_ONE
        move_completed = 0
       
    elif (incomingString == "displace_2"):
        state = DISPLACE_TWO
        move_completed = 0


### Global definitions
INTER_COMMAND_DELAY = 4

HOME = 6
PINCH_ONE = 7
PINCH_TWO = 8
DISPLACE_ONE = 1
DISPLACE_TWO = 2
START = 3

state = HOME
move_completed = 0
### end global definitions

def pinch_test_arm_control():
    """
    Function to demonstrate moving the ur5 to home pose
    """
    # Initialize the ros node
    rospy.init_node("pinch_test_arm_control", anonymous=True, disable_signals=True)
    
    # Setup subscription to cmd_motor_controller topic
    rospy.Subscriber("master_state", String, state_callback)
    
    # Publish just z position for plotting later
    z_pos_pub = rospy.Publisher('ur5_position', z_pos, queue_size=10)

    # Instantiate the UR5 interface.
    ur5 = UR5Interface()
    
    ur5.goto_home_down()
    home_pose = ur5.get_pose()
    move_completed = 1
    
    while not rospy.is_shutdown(): 
        
        global move_completed
        
        if (move_completed == 0):
            
            OFFSET_VALUE = 0.005
            FULL_DISPLACEMENT = 0.02
            
            if (state == HOME): 
                print("Moving to home position")
                ur5.set_speed(.1)
                ur5.goto_home_down()
                home_pose = ur5.get_pose()
                move_completed = 1
                
            elif (state == START): 
                print("Moving to start position")
                start_pose = copy.deepcopy(home_pose)
                ur5.set_speed(.1)
                start_pose.position.z -= 0.09
                ur5.goto_pose_target(start_pose, wait = False)
                move_completed = 1
            
            elif (state == DISPLACE_ONE): 
                print("Performing first displacement")
                ur5.set_speed(.01)
                first_pose = copy.deepcopy(start_pose)
                first_pose.position.z += OFFSET_VALUE
                ur5.goto_pose_target(first_pose, wait = False)
                move_completed = 1
            
            elif (state == DISPLACE_TWO): 
                print("Performing second displacement")
                ur5.set_speed(.01)
                second_pose = copy.deepcopy(start_pose)
                second_pose.position.z += FULL_DISPLACEMENT
                ur5.goto_pose_target(second_pose, wait = False)
                move_completed = 1
                
        cur_pose = ur5.get_pose()
        cur_z_pos = cur_pose.position.z
        z_pos_pub.publish(cur_z_pos)        


if __name__ == '__main__': 
    pinch_test_arm_control()
