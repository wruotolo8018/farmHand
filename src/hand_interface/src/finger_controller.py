#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String, Int16
import serial
import time
import numpy as np
from hand_interface.msg import flex_sns

# state definitions
MOVE_TO_POSE_1 = 2
MOVE_TO_POSE_2 = 3
MOVE_TO_POSE_3 = 4
TIGHTEN = 5
LOOSEN = 6
STOPPED = 0
PURE_CONTACT_CONTROL = 1

state = STOPPED

# Useful saved motor values
stop_motor_string = "505050505050505050"
forward_motor_string = "505050606060505050"
backward_motor_string = "505050404040505050"
stop_motor_array = np.array([0,0,0,0,0,0,0,0,0])

# Basic sensor data variables
cur_joint_data = np.zeros(6)
prev_joint_data = np.zeros(6)

# Temp substate
NOT_GRASPING = 0
GRASP_START = 1
GRASP_LATER = 2
grasp_substate = NOT_GRASPING
grasp_start_time = 0

# PWM variables
pos_pwm_array = np.zeros(6)
cur_pwm_array = np.zeros(6)



# Accessory function to conveniently map one range of values to another
def arduino_map(val, inMin, inMax, outMin, outMax):
    return int((val-inMin)*(outMax-outMin)/(inMax-inMin)+outMin)

# Callback functions    
def state_callback(data):
    incomingString = str(data.data)
    global state
#    print("Incoming command: " + incomingString)
    
    if (incomingString == "move_to_pose_1"):
        state = MOVE_TO_POSE_1
        print("Switching state to MOVE_TO_POSE_1")
    elif (incomingString == "move_to_pose_2"):
        state = MOVE_TO_POSE_2
        print("Switching state to MOVE_TO_POSE_2")
    elif (incomingString == "move_to_pose_3"):
        state = MOVE_TO_POSE_3
        print("Switching state to MOVE_TO_POSE_3")
    elif (incomingString == "stop"):
        state = STOPPED
        print("Switching state to STOPPED")
    elif (incomingString == "tighten"):
        state = TIGHTEN
        print("Switching state to TIGHTEN")
    elif (incomingString == "loosen"):
        state = LOOSEN
        print("Switching state to LOOSEN")
    elif (incomingString == "pure_contact"):
        state = PURE_CONTACT_CONTROL
        print("Switching state to PURE_CONTACT_CONTROL")
    
# Callback function for joint position sensing data
def joint_sns_callback(data):
    # Bump old data to prev variable
    global prev_joint_data, cur_joint_data
    prev_joint_data = cur_joint_data
    # Finger 1
    cur_joint_data[0] = data.prox1
    cur_joint_data[1] = data.dist1
    # Finger 2
    cur_joint_data[2] = data.prox2
    cur_joint_data[3] = data.dist2
    # Finger 3
    cur_joint_data[4] = data.prox3
    cur_joint_data[5] = data.dist3

# Convert array of pwm ints to single string format for serial transmission
# and center around 50 instead of 0
def pwm_array_to_string(pwm_array):
    pwm_string = ""
    # Center around 50 for transmission without negatives
    pwm_array_temp = pwm_array + 50
    # Modify values to ensure 2 digits for each
    for val in pwm_array_temp:
        if (val > 99):
            val = 99
        elif (val < 0):
            val = 0
        if (val < 10):
            pwm_string = pwm_string + "0" + str(int(val))
        else:
            pwm_string = pwm_string + str(int(val))
    return pwm_string

# Accessory function to handle pwm capping at various stages
def pwm_cap(pwmVal, capVal):
    if (pwmVal < -capVal):
        pwmVal = -capVal
    elif (pwmVal > capVal):
        pwmVal = capVal
    return pwmVal    
    
# Accessory function to implement deadzones for stability
def process_deadzone(pwmVal, deadzone_val):
    if (pwmVal < deadzone_val and pwmVal > -deadzone_val):
        pwmVal = 0
    return pwmVal

# Simple PID (really just P rn) control function to update pwm values based on sensed joint angles
def position_control(des_prox, des_dist, fing_num):
    # Access global variables
    global cur_joint_data, pos_pwm_array, cur_pwm_array
    
    # Set control variables
    kp_scale = .1
    kp1 = 1.0
    kp2 = 1.0
    looseScale = 0.75
    one_dir_deadzone = 0 # In PWM/2, not sensor values
    prox_index = fing_num*2
    dist_index = fing_num*2+1
    
    # Run proportional control law
    prox_error = kp_scale*(des_prox - cur_joint_data[prox_index])
    dist_error = kp_scale*(des_dist - cur_joint_data[dist_index])
    
    Cpwm = 0
    Upwm = 0
    
    if (des_prox > 0 and des_dist < 0):    
        ######## Working hyperextension controller (two directional)
        Cpwm = int(kp1*prox_error)
        Upwm = -int(kp2*prox_error + kp1*dist_error)
        
        Cpwm = pwm_cap(Cpwm,40)
        Upwm = pwm_cap(Upwm,40)
    
        if (Cpwm < 0):
            Cpwm = Cpwm*looseScale
            Cpwm = pwm_cap(Cpwm,20)
        if (Upwm < 0):
            Upwm = Upwm*looseScale
            Upwm = pwm_cap(Upwm,20)
        ######### End of hyperextension controller
    elif (des_prox > 0 and des_dist > 0):
        ######### Curling Controller
        prox_threshold = 10
#        if(np.absolute(prox_error) > prox_threshold):
        Cpwm = int(prox_error + dist_error)
        Upwm = -int(prox_error + dist_error)
        print("adjusting prox joint")
#        else:
#            Cpwm = int(dist_error)
#            Upwm = -int(prox_error + dist_error)
#            print("adjusting distal joint")
        ######### End of curling controller
    elif (des_prox == 0 and des_dist == 0): 
        ######### Curling Controller
        prox_threshold = 10
        if(np.absolute(prox_error) > prox_threshold):
            Cpwm = int(prox_error)
            Upwm = -int(prox_error)
            print("adjusting prox joint")
        else:
#            Cpwm = int(prox_error + dist_error)
            Upwm = -int(dist_error)
            print("adjusting distal joint")
        ######### End of curling controller
    
    
    #    Cpwm = int(prox_error)
#    Upwm = -int(prox_error)
#    
    
        

    
#    if (np.sign(prox_error) == np.sign(dist_error)):
#        # curling condition
#        Cpwm = int(prox_error + dist_error)
#        Upwm = int(prox_error)
#        print("curling") 
#        
#        Cpwm = int(prox_error)
#        Upwm = -int(prox_error)
#        
#        prox_threshold = 50
#        if(np.absolute(prox_error) > prox_threshold):
#            Cpwm = int(prox_error)
#            Upwm = -int(prox_error)
#            print("adjusting prox joint")
#        else:
#            Cpwm = int(prox_error + dist_error)
#            Upwm = -int(prox_error + dist_error)
#            print("adjusting distal joint")
#         
#    else:    
#        Cpwm = int(kp1*prox_error) #  + kp2*dist_error)
#        Upwm = -int(kp2*prox_error + kp1*dist_error)
#        print("hyperextending")
    
#    if(prox_error > 0):
#        Cpwm = int(prox_error + dist_error)
#        Upwm = -int(prox_error)
#        print("+ prox error")
#    elif(prox_error < 0):
#        Cpwm = int(prox_error)
#        Upwm = -int(prox_error + dist_error)
#        print("- prox error")
    
#    Cpwm = int(kp1*prox_error) #  + kp2*dist_error)
#    Upwm = -int(kp2*prox_error + kp1*dist_error)
#    
#    
    
#    Cpwm = int(kp_scale*(kp1*(des_prox - cur_joint_data[prox_index]) + kp2*(des_dist - cur_joint_data[dist_index])))
#    Upwm = int(kp_scale*(-(kp2*(des_prox - cur_joint_data[prox_index]) + kp1*(des_dist - cur_joint_data[dist_index]))))

    
    
    
    
    # Apply a deadzone if needed for stability (was originally working fine without)
    Cpwm = process_deadzone(Cpwm, one_dir_deadzone)
    Upwm = process_deadzone(Upwm, one_dir_deadzone)
            
    # Set pwm array values based on updates
    pos_pwm_array[fing_num*2 : fing_num*2+2] = [Cpwm, Upwm]
    cur_pwm_array[fing_num*2 : fing_num*2+2] = pos_pwm_array[fing_num*2 : fing_num*2+2]
    
    # Print updated pwm array for debugging
    # print(pos_pwm_array)


# Final safety function to put a cap on max PWM
def final_pwm_cap(one_dir_final_cap):
    # Access global variables
    global cur_pwm_array
    # Iterate through PWM array, apply cap, and shift center
    for i in range(len(cur_pwm_array)):
        cur_pwm_array[i] = pwm_cap(cur_pwm_array[i], one_dir_final_cap)


# Main loop
def motor_controller():
    
    # Setup node
    rospy.init_node('motor_serial_interface', anonymous=True)
    
    # Setup subscription to cmd_motor_controller topic
    rospy.Subscriber("master_state", String, state_callback)
    rospy.Subscriber("flex_sensors", flex_sns, joint_sns_callback)   
    
    cmdPub = rospy.Publisher('motor_cmd', String, queue_size=10)
     
    # Global variables
    global cur_pwm_array, cur_des_pose, grasp_substate, grasp_start_time, w_p, w_c, w_f
    print("Start PWM ARRAY: " + str(cur_pwm_array))
    
    # Set loop speed
    rate = rospy.Rate(50) #50hz
    
    # Output that things are going
    print("Running motor_controller node.")

    while not rospy.is_shutdown():  
        # Internal state machine sets pwm array based on state and sensed values
        if (state == MOVE_TO_POSE_1):

            grasp_substate = NOT_GRASPING

            # Define desired position values for testing
            des_prox_value = 0
            des_dist_value = 0
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
#            position_control(des_prox_value, des_dist_value, 1)
#            position_control(des_prox_value, des_dist_value, 2)
            
            # Cap final pwm value 
            final_pwm_cap(30);
        
        elif (state == MOVE_TO_POSE_2):
            # Define desired position values for testing
            des_prox_value = 400
            des_dist_value = 600
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
#            position_control(des_prox_value, des_dist_value, 1)
#            position_control(des_prox_value, des_dist_value, 2)
           
            # Cap final pwm value 
            final_pwm_cap(30);
        
        elif (state == MOVE_TO_POSE_3):
            # Define desired position values for testing
            des_prox_value = 900
            des_dist_value = -700
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
#            position_control(des_prox_value, des_dist_value, 1)
#            position_control(des_prox_value, des_dist_value, 2)
                        
            # Cap final pwm value 
            final_pwm_cap(30);   
       
        elif (state == PURE_CONTACT_CONTROL):
            dummyVar = 1
        
        elif (state == TIGHTEN):
            cur_pwm_array[:] = [10,10,10,10,10,10,10,10,10]
        
        elif (state == LOOSEN):
            cur_pwm_array[:] = [-10,-10,-10,-10,-10,-10,-10,-10,-10]
        
        # Process pwm array into string for serial comms
        cur_motor_string = pwm_array_to_string(cur_pwm_array)
        
        # Final safety check for stopped conditions
        if (state == STOPPED): 
            cmdPub.publish(stop_motor_string)
            cur_motor_string = stop_motor_string
            cur_pwm_array = stop_motor_array
        
        # Print current motor pwm values and resulting string for debugging purposes
#        print("PWM Array: " + str(cur_pwm_array))
#        print("Current motor string: " + cur_motor_string)
        
        # Publish current motor string for motor interface to handle
        cmdPub.publish(cur_motor_string)
        
        # Sleep to maintain command update rate
        rate.sleep()

if __name__ == '__main__':
    try:
        motor_controller()
    except rospy.ROSInterruptException:
        pass