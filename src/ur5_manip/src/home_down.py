#!/usr/bin/env python

import os
import sys
import time
import rospy
import numpy as np
import copy

from ur5_interface import UR5Interface

### end global definitions

def move_home():

    # Initialize the ros node
    rospy.init_node("test_move_home", anonymous=True, disable_signals=True)

    # Instantiate the UR5 interface.
    ur5 = UR5Interface()

    # go to home and print the joint values
    ur5.goto_home_pose()
#    home_pose = ur5.get_pose()
#    home_pose.position.z += .1
#    home_pose.position.y += .1
#    
#    ur5.goto_pose_target(home_pose)
    
    
    print(ur5.get_joint_values())

if __name__ == '__main__': 
    move_home()
