#!/usr/bin/env python

import os
import sys
import time
import rospy
import numpy as np
import copy
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply

from ur5_interface import UR5Interface

### end global definitions

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

def move_home():

    # Initialize the ros node
    rospy.init_node("test_move_home", anonymous=True, disable_signals=True)

    # Instantiate the UR5 interface.
    ur5 = UR5Interface()

    # go to home and print the joint values
    ur5.goto_home_pose()
    home_pose = ur5.get_pose()
    
    front_pose = copy.deepcopy(home_pose)
    print(front_pose)
    
    quat_15x = quaternion_from_euler(3.14159/12*2,0,0)
    og_quat = get_quaternion(front_pose)
    print(og_quat)
    
    new_quat = quaternion_multiply(quat_15x, og_quat)
    front_pose = set_quaternion(front_pose,new_quat)
    front_pose.position.z += .05
    print(front_pose)
    
    ur5.goto_pose_target(front_pose)
    
    new_quat = quaternion_multiply(quat_15x, new_quat)
    front_pose = set_quaternion(front_pose,new_quat)
    front_pose.position.z += .05
    ur5.goto_pose_target(front_pose)
        
    
    print(ur5.get_joint_values())

if __name__ == '__main__': 
    move_home()
