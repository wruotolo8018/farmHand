#!/usr/bin/env python

import os
import sys
import time
import rospy
import numpy as np
import copy
from ur5_interface import UR5Interface
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply

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


### end global definitions

def move_home():

    # Initialize the ros node
    rospy.init_node("test_move_home", anonymous=True, disable_signals=True)

    # Instantiate the UR5 interface.
    ur5 = UR5Interface()

    # go to home and print the joint values
    ur5.set_speed(0.1)
    ur5.goto_home_down()

    maintenance_pose = ur5.get_pose()
    quat = quaternion_from_euler(0, -3.14159, 0)
    og_quat = get_quaternion(maintenance_pose)
    new_quat = quaternion_multiply(quat, og_quat)
    maintenance_pose = set_quaternion(maintenance_pose, new_quat)
    maintenance_pose.position.y += 0.3
    ur5.goto_pose_target(maintenance_pose, wait=False)
    
    print(ur5.get_joint_values())

if __name__ == '__main__': 
    move_home()
