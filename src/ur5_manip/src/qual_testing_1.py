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
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from ur5_interface import UR5Interface

### Global definitions
INTER_COMMAND_DELAY = 4

HOME = 0
START = 1
MOVE_1 = 2
MOVE_2 = 3
MOVE_3 = 4
MOVE_4 = 5
MOVE_5 = 6
MOVE_6 = 7
MOVE_7 = 8
MOVE_8 = 9
MOVE_9 = 10
MOVE_10 = 11
MOVE_11 = 12
MOVE_12 = 13

state = HOME
move_completed = 0

pose_x, pose_y, pose_z = 0.0, 0.0, 0.0
eul_1, eul_2, eul_3 = 0.0, 0.0, 0.0

### end global definitions

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


        
    elif (incomingString == "move_1"):
        state = MOVE_1
        move_completed = 0
       
    elif (incomingString == "move_2"):
        state = MOVE_2
        move_completed = 0

    elif (incomingString == "move_3"):
        state = MOVE_3
        move_completed = 0

    elif (incomingString == "move_4"):
        state = MOVE_4
        move_completed = 0

    elif (incomingString == "move_5"):
        state = MOVE_5
        move_completed = 0

    elif (incomingString == "move_6"):
        state = MOVE_6
        move_completed = 0

    elif (incomingString == "move_7"):
        state = MOVE_7
        move_completed = 0

    elif (incomingString == "move_8"):
        state = MOVE_8
        move_completed = 0

def set_quaternion(pose, quaternion):
    pose.orientation.x = quaternion[0]
    pose.orientation.y = quaternion[1]
    pose.orientation.z = quaternion[2]
    pose.orientation.w = quaternion[3]
    return pose

def get_quaternion(pose):
    quat = np.zeros(4)
    quat[0] = pose.orientation.x
    quat[1] = pose.orientation.y
    quat[2] = pose.orientation.z
    quat[3] = pose.orientation.w
    return quat

def relative_pose(old_pose, x_dot, y_dot, z_dot, eul_1, eul_2, eul_3):
    new_pose = copy.deepcopy(old_pose)
    delta_quat = quaternion_from_euler(eul_1, eul_2, eul_3)
    og_quat = get_quaternion(old_pose)
    new_quat = quaternion_multiply(delta_quat, og_quat)
    new_pose = set_quaternion(new_pose, new_quat)
    new_pose.position.x += x_dot
    new_pose.position.y += y_dot
    new_pose.position.z += z_dot
    return new_pose


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
                start_pose.position.z += 0.1
                ur5.goto_pose_target(start_pose, wait = False)
                move_completed = 1
            
            elif (state == MOVE_1):
                print("Performing first movement")
                ur5.set_speed(.05)
                pose_1 = relative_pose(home_pose, 0, 0, -0.023, 0, 0, 0)
                ur5.goto_pose_target(pose_1, wait = False)
                move_completed = 1
            
            elif (state == MOVE_2):
                print("Performing second movement")
                pose_2 = relative_pose(pose_1, 0, 0, .1, 0,0,0)
                ur5.goto_pose_target(pose_2, wait = False)
                move_completed = 1

            elif (state == MOVE_3):
                print("Performing third movement")
                ur5.set_speed(.15)
                pose_3 = relative_pose(pose_2, 0,0,0,0,0,-3.14159/2)
                ur5.goto_pose_target(pose_3, wait = False)
                move_completed = 1

            elif (state == MOVE_4):
                print("Performing fourth movement")
                ur5.set_speed(.15)
                pose_4 = relative_pose(pose_3, 0, 0, 0, 0, 0, 3.14159/2)
                ur5.goto_pose_target(pose_4, wait=False)
                move_completed = 1

            elif (state == MOVE_5):
                print("Performing fifth movement")
                ur5.set_speed(.05)
                pose_4 = relative_pose(pose_4, 0, .1, 0, 3.14159 / 4, 0, 0)
                ur5.goto_pose_target(pose_4, wait=False)
                move_completed = 1

            elif (state == MOVE_6):
                print("Performing sixth movement")
                move_completed = 1

            elif (state == MOVE_7):
                print("Performing seventh movement")
                move_completed = 1

            elif (state == MOVE_8):
                print("Performing eighth movement")
                move_completed = 1


if __name__ == '__main__': 
    pinch_test_arm_control()
