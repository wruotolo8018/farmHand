#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from ur5_interface import UR5Interface

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

# Setup global variables
state_string = "manual_input"

def master_state_machine():
    
    # Set up publisher to master_state topic
    pub_master_state = rospy.Publisher('master_state', String, queue_size=10)
    
    # State node at 10hz (speed should be flexible)
    rospy.init_node('master_state_machine', anonymous=True)
#    rate = rospy.Rate(10) # 10hz

    # Instantiate the UR5 interface.
    ur5 = UR5Interface()
    # ur5.goto_home_down()
    home_pose = ur5.get_pose()
    
    # Enter main control loop (this is blocking based on user input right now)
    while not rospy.is_shutdown():
        # Display control options
        print('Enter a Command:')
        print('[space] = stop all motors')
        print('[1] = home fingers')
        print('[2] = test pregrasp')
        print('[3] = test grasp')
        print('[4] = tighten tendons')
        print('[5] = loosen tendons')
        print('[6] = start grasp sequence')
        print('[0] = home arm')
        input_string = raw_input('Input: ')
        
        # Handle input and publish appropriate state
        if (input_string == ' '):
            state_string = "stop"
            pub_master_state.publish(state_string)
        elif (input_string == '1'):
            state_string = "home_fingers"
            pub_master_state.publish(state_string)
        elif (input_string == 'q'):
            state_string = "grasp_1"
            pub_master_state.publish(state_string)
        elif (input_string == 'w'):
            state_string = "grasp_2"
            pub_master_state.publish(state_string)
        elif (input_string == 'e'):
            state_string = "grasp_3"
            pub_master_state.publish(state_string)
        elif (input_string == '4'):
            state_string = "tighten"
            pub_master_state.publish(state_string)
        elif (input_string == '5'):
            state_string = "loosen"
            pub_master_state.publish(state_string)
        elif (input_string == '0'):
            ur5.set_speed(.1)
            ur5.goto_home_down()
        elif (input_string == 'x'):
            old_pose = ur5.get_pose()
            while (True):
                user_input = raw_input("X change: ")
                if (user_input == ' '):
                    break
                change = float(user_input)
                new_pose = relative_pose(old_pose, change, 0, 0, 0, 0, 0)
                ur5.goto_pose_target(new_pose, wait=False)
                old_pose = new_pose
        elif (input_string == 'y'):
            old_pose = ur5.get_pose()
            while (True):
                user_input = raw_input("Y change: ")
                if (user_input == ' '):
                    break
                change = float(user_input)
                new_pose = relative_pose(old_pose, 0, change, 0, 0, 0, 0)
                ur5.goto_pose_target(new_pose, wait=False)
                old_pose = new_pose
        elif (input_string == 'z'):
            old_pose = ur5.get_pose()
            while (True):
                user_input = raw_input("Z change: ")
                if (user_input == ' '):
                    break
                change = float(user_input)
                new_pose = relative_pose(old_pose, 0, 0, change, 0, 0, 0)
                ur5.goto_pose_target(new_pose, wait=False)
                old_pose = new_pose





        elif (input_string == '6'):
            # Start grasp sequence
            # Press enter to step through sequence
            # Type space to break out of sequence and stop fingers
            # Type 'b' to go backwards a step

            print("\nTesting sequence started!\n")

            num_steps = 15
            step = 0
            manual_stepping = True
            while (step <= num_steps):
                if (manual_stepping):
                    user_input = raw_input("\nENTER for next step, type 'b' for previous, and ' ' for stop: ")
                else:
                    user_input = 'auto'

                # Handle user input to step through demo sequence
                if (user_input == ''):
                    step += 1
                elif (user_input == 'b'):
                    step -= 1
                elif (user_input == ' '):
                    # Stop everything
                    print("Halting test sequence!")
                    break
                elif (user_input == 'auto'):
                    # Do nothing
                    print("Automatically stepping")
                elif (user_input == '1'):
                    state_string = "home_fingers"
                    pub_master_state.publish(state_string)
                elif (input_string == '4'):
                    state_string = "tighten"
                    pub_master_state.publish(state_string)
                elif (input_string == '5'):
                    state_string = "loosen"
                    pub_master_state.publish(state_string)
                elif (input_string == '2'):
                    state_string = "pregrasp_wide"
                    pub_master_state.publish(state_string)
                elif (input_string == '3'):
                    state_string = "grasp_wide"
                    pub_master_state.publish(state_string)


                # Handle arm movement situation for each step
                if (step == 1):
                    print("Going to start position")
                    start_pose = relative_pose(home_pose, 0, 0, 0, 0, 0, -3.14159/2)
                    ur5.goto_pose_target(start_pose, wait=False)
                elif (step == 2):
                    print("Pregrasping")
                    pub_master_state.publish("pregrasp_wide")
                elif (step == 3):
                    print("Going to second position")
                    pose_2 = relative_pose(start_pose, 0, 0, -0.14, 0, 0, 0)
                    ur5.goto_pose_target(pose_2, wait=False)
                elif (step == 4):
                    print("Grasping")
                    pub_master_state.publish("grasp_wide")
                elif (step == 5):
                    print("Picking up")
                    pose_3 = relative_pose(pose_2, 0, 0, 0.1, 0, 0, 0)
                    ur5.goto_pose_target(pose_3, wait=False)
                elif (step == 6):
                    print("Rotating")
                    pose_4 = relative_pose(pose_3, 0, 0, -.1, 0, 3.14159/2, 0)
                    ur5.goto_pose_target(pose_4, wait=False)
                elif (step == 7):
                    print("Placing")
                    pose_5 = relative_pose(pose_4, -.1, 0, -.12, 0, 0, 0)
                    ur5.goto_pose_target(pose_5, wait=False)
                elif (step == 8):
                    print("Releasing")
                    pub_master_state.publish('grasp_4')
                elif (step == 9):
                    print("Leaving")
                    pose_6 = relative_pose(pose_5, 0, 0, .1, 0, 0, 0)
                    ur5.goto_pose_target(pose_6, wait=False)



        # print("Test sequence ended. Halting fingers.")
        # state_string = "stop"
        # pub_master_state.publish(state_string)




            #
            #
            #
            # raw_input("Go to home? Press Enter")
            # state_string = "home_arm"
            # pub_master_state.publish(state_string)
            #
            # # # Open wide for plate
            # # raw_input("Pregrasp?")
            # # print("Pregrasping")
            # # state_string = "pregrasp_wide"
            # # pub_master_state.publish(state_string)
            #
            # # Go down to plate
            # raw_input("Start trial? Press Enter")
            # state_string = "start"
            # pub_master_state.publish(state_string)
            #
            # # Grab plate
            # raw_input("Start grasping? Press Enter")
            # state_string = "grasp_pinch"
            # pub_master_state.publish(state_string)
            #
            # # Go back up
            # raw_input("Go to position 1? Press Enter")
            # print("Performing displacement 1")
            # state_string = "move_1"
            # pub_master_state.publish(state_string)
            #
            # # Rotate and go above dish rack
            # raw_input("Go to position 2? Press Enter")
            # print("Going to position 2 and grasping")
            # state_string = "move_2"
            # pub_master_state.publish(state_string)
            #
            # # Go to shelf
            # raw_input("Go to position 3? Press Enter")
            # print("Going to position 3")
            # state_string = "move_3"
            # pub_master_state.publish(state_string)
            #
            # # Release plate
            # # Handled in parallel on other state machine
            #
            # # Go back to home
            # raw_input("Press Enter")
            # # state_string = "home_fingers"
            # # pub_master_state.publish(state_string)
            # state_string = "move_4"
            # pub_master_state.publish(state_string)



if __name__ == '__main__':
    try:
        master_state_machine()
    except rospy.ROSInterruptException:
        pass