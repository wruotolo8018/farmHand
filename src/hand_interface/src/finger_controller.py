#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String, Int16
import serial
import time
import numpy as np
from tae_psoc.msg import SensorPacket, cmdToPsoc, Sensor_Fast, Sensor_Indiv
from basic_sensor_interface.msg import tendon_sns, joint_sns

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
cur_tendon_data = np.zeros(9)
prev_tendon_data = np.zeros(9)
tendon_binary_engagement = np.zeros(9)
tendon_binary_cutoff = np.array([0,0,0,100,100,200,0,0,0])
cur_joint_data = np.zeros(6)
prev_joint_data = np.zeros(6)

# Temp substate
NOT_GRASPING = 0
GRASP_START = 1
GRASP_LATER = 2
grasp_substate = NOT_GRASPING
grasp_start_time = 0

# Nib sensor data variables
cur_nib_data = np.zeros(36*3)
prev_nib_data = np.zeros(36*3)

# PWM variables
pos_pwm_array = np.zeros(9)
contact_pwm_array = np.zeros(9)
force_pwm_array = np.zeros(9)
tension_pwm_array = np.zeros(9)
cur_pwm_array = np.zeros(9)

# State controller weights
w_p = 0
w_c = 0
w_f = 0

# Contact working variables
prev_x_c_scaled = np.zeros(3) 
integral_error = np.zeros(3)
integral_error_fg = np.zeros(3)


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
        
        
# Callback function for nib sensor in individual mode
def nib_sns_callback(data):
    # Bump old data to prev variable
    global cur_nib_data, prev_nib_data
    prev_nib_data = cur_nib_data
    
    # Finger 1
    cur_nib_data[0:36] = np.asarray(data.sns_1_Indiv)
    
    # Thumb
    cur_nib_data[36:36*2] = np.asarray(data.sns_2_Indiv)
    
    # Finger 2
    cur_nib_data[36*2:36*3] = np.asarray(data.sns_3_Indiv)
    
    
# Callback function for tendon force sensing data     
def tendon_sns_callback(data):
    # Bump old data to prev variable
    global prev_tendon_data, cur_tendon_data
    prev_tendon_data = cur_tendon_data
    # Fill cur_tendon_data with updated data
    # Finger 1
    cur_tendon_data[0] = data.prox1
    cur_tendon_data[1] = data.dist1
    cur_tendon_data[2] = data.hype1
    # Finger 2
    cur_tendon_data[3] = data.prox2
    cur_tendon_data[4] = data.dist2
    cur_tendon_data[5] = data.hype2
    # Thumb
    cur_tendon_data[6] = data.prox3
    cur_tendon_data[7] = data.dist3
    cur_tendon_data[8] = data.hype3
    
    # Go through and set binary values for taught or not
    for i in range(9):
        if (cur_tendon_data[i] > tendon_binary_cutoff[i]):
            tendon_binary_engagement[i] = 1
        else:
            tendon_binary_engagement[i] = 0
    
    
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
    # Thumb
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
    global cur_joint_data, pos_pwm_array
    
    # Set control variables
    kp1 = 0.2
    kp2 = 0.2 
    looseScale = 0.9
    one_dir_pmw_cap = 30 # In PWM/2, not sensor values
    one_dir_deadzone = 0 # In PWM/2, not sensor values
    prox_index = fing_num*2
    dist_index = fing_num*2+1
    
    # Run basic proportional control law
    Ppwm = int(kp1*(des_prox - cur_joint_data[prox_index]))
    Dpwm = int(kp2*(des_dist - cur_joint_data[dist_index]))
    Hpwm = int(-(kp1*(des_prox - cur_joint_data[prox_index]) + kp2*(des_dist - cur_joint_data[dist_index])))

    if (Ppwm < 0):
        Ppwm = Ppwm*looseScale
    if (Dpwm < 0):
        Dpwm = Dpwm*looseScale
    if (Hpwm < 0):
        Hpwm = Hpwm*looseScale*.1
        
    # Cap pwm to max for component safety (there should be another larger cap at end of controls)
    Ppwm = pwm_cap(Ppwm, one_dir_pmw_cap)
    Dpwm = pwm_cap(Dpwm, one_dir_pmw_cap)
    Hpwm = pwm_cap(Hpwm, one_dir_pmw_cap)
    
    # Apply a deadzone if needed for stability (was originally working fine without)
    Ppwm = process_deadzone(Ppwm, one_dir_deadzone)
    Dpwm = process_deadzone(Dpwm, one_dir_deadzone)
    Hpwm = process_deadzone(Hpwm, one_dir_deadzone)
    
    # Set pwm array values based on updates
    pos_pwm_array[fing_num*3 : fing_num*3+3] = [Ppwm, Dpwm, Hpwm]
    
    # Print updated pwm array for debugging
    # print(pos_pwm_array)


# Simple PID control on contact pressure centroid
def contact_control(des_xc, fing_num):
    # Get global sensor data access
    global cur_nib_data, prev_nib_data, prev_x_c_scaled, integral_error
    
    # Position Controller
    nib_top_avg = np.average(cur_nib_data[fing_num*36:18+fing_num*36])
    nib_bottom_avg = np.average(cur_nib_data[18+fing_num*36:36+fing_num*36])
    k_temp = 0.2
    x_c_scaled = k_temp*(nib_top_avg - nib_bottom_avg)
    # Scale top and bottom for ad hoc calibration
    if (x_c_scaled < 0):
        x_c_scaled = x_c_scaled*0.3
#    print("x_c_scaled value: " + str(x_c_scaled))
    
    # Derivative control stuff
    k_d = 5.0
    x_c_delta = k_d * (x_c_scaled - prev_x_c_scaled[fing_num])
    prev_x_c_scaled[fing_num] = x_c_scaled
    
    # Integral Control stuff
    integral_windup = 500
    k_i = 0.0
    integral_x_c_deadzone = 5
    if not (np.absolute(x_c_scaled) < integral_x_c_deadzone):
        integral_error[fing_num] = (integral_error[fing_num] + x_c_scaled)
    if (integral_error[fing_num] > integral_windup): 
        integral_error[fing_num] = integral_windup
    elif (integral_error[fing_num] < -integral_windup):
        integral_error[fing_num] = -integral_windup
    integral_error_scaled = k_i * integral_error[fing_num]
#    print("Integral control value: " + str(integral_error_scaled))
        
        
    # Basic control law
    # if x_c is positive, we want to hyperextend
    # if x_c is negative, we want to curl more
#    relative_scale = 1
    Ppwm = int(x_c_scaled + x_c_delta + integral_error_scaled)
    Dpwm = int(-x_c_scaled - x_c_delta - integral_error_scaled)
    # Try holding constant???
    Hpwm = int(0)
    # Or maintain constant tension
    
    # Apply a deadzone if needed for stability (was originally working fine without)
    one_dir_deadzone = 15
    Ppwm = process_deadzone(Ppwm, one_dir_deadzone)
    Dpwm = process_deadzone(Dpwm, one_dir_deadzone)
    Hpwm = process_deadzone(Hpwm, one_dir_deadzone)
    
    # Set pwm array values based on updates
    contact_pwm_array[fing_num*3 : fing_num*3+3] = [Ppwm, Dpwm, Hpwm]
    
    
        
    
# Simple PID control grasp force
def grasp_force_control(des_fn, fing_num):
    # Get global sensor data access
    global cur_nib_data, prev_nib_data, integral_error_fg, grasp_substate
    
    # TODO: adjust contact_pwm_array based on pressure centroid
    full_avg = np.average(cur_nib_data[fing_num*36:36+fing_num*36])
    if (full_avg < 0):
        full_avg = 0            
#    print("Full average: " + str(full_avg))
    
    # Basic control law
    # Exert a positive torque on each proportional to contact location
    # Orrrr just clamp harder
    relative_scale = 0.5
    k_temp = 0.2
    
    k_i = 0.02
    integral_windup = 5000
    des_fn = 300
    force_val = (des_fn - full_avg)
#    print("Raw force value for finger " + str(fing_num) + ": " + str(force_val))
    force_val_scaled = k_temp*force_val
    
    # Integral Control stuff
    force_update_deadzone = 5
    if not (np.absolute(force_val_scaled) < force_update_deadzone): # Apply mini deadzone
        integral_error_fg[fing_num] = (integral_error_fg[fing_num] + force_val) # Main error integration
    # Apply windup limit
    if (integral_error_fg[fing_num] > integral_windup): 
        integral_error_fg[fing_num] = integral_windup
    elif (integral_error_fg[fing_num] < -integral_windup):
        integral_error_fg[fing_num] = -integral_windup
    integral_error_scaled = k_i * integral_error_fg[fing_num]
    # Debug print
#    print("Integral control value: " + str(integral_error_scaled))
    # Update PWM Commands
    Ppwm = int(force_val_scaled + integral_error_scaled)
    Dpwm = int(force_val_scaled + integral_error_scaled)
    # Try blind value = negative of others
#    Hpwm = -int(force_val_scaled + integral_error_scaled)*relative_scale
    
    # Depending on substate either loosen tendon or hold constant
    if grasp_substate == GRASP_START:
        print("In grasp start phase")
        Hpwm = -30
    else:
        print("In else statement for other grasping")
        Hpwm = 0
    
    # Apply a deadzone if needed for stability (was originally working fine without)
    one_dir_deadzone = 0
    Ppwm = process_deadzone(Ppwm, one_dir_deadzone)
    Dpwm = process_deadzone(Dpwm, one_dir_deadzone)
    Hpwm = process_deadzone(Hpwm, 30)
    
    # Set pwm array values based on updates
    force_pwm_array[fing_num*3 : fing_num*3+3] = [Ppwm, Dpwm, Hpwm]
   
    
# Tendon sensing adaptor to prevent tendon laxity 
def tendon_tension_control(fing_num):
    # Access global variables
    global cur_tendon_data, cur_pwm_array, tendon_binary_cutoff, tendon_binary_engagement, tension_pwm_array
    
    # Set Control variables
    binary_gain = 30
    
    # Go through tendon tension sensors and modifty to tighten if loose
    # TODO: Debug
    prox_index = fing_num*3
    dist_index = fing_num*3+1
    hype_index = fing_num*3+2
    for i in range(prox_index, hype_index):
        # If loose, tighten
        if (tendon_binary_engagement[i] == 0):
            tension_pwm_array[i] = binary_gain
            print("Tendon tension controller activated")
        # If already tense, do nothing
        else:
            tension_pwm_array[i] = 0
    # Add binary adjustments to cur_pwm_array for processing before pwm cap
    for i in range(len(cur_pwm_array)):
#        if ((i+1) % 3 == 0):
        cur_pwm_array[i] += float(tension_pwm_array[i])
    

def gain_filter(fing_num):
    # Access global variables
    global pos_pwm_array, contact_pwm_array, force_pwm_array, cur_pwm_array
    global w_p, w_c, w_f
    
    # TODO: Define control variables based on state
#    w_p = 1
#    w_c = 0
#    w_f = 0
    
    # Create manipulation matrices
    prox_index = fing_num*3
    dist_index = fing_num*3+1
    hype_index = fing_num*3+2
    
    # Build full vector of possible pwm values
    pos_vec = pos_pwm_array[prox_index:hype_index+1]
    contact_vec = contact_pwm_array[prox_index:hype_index+1]
    force_vec = force_pwm_array[prox_index:hype_index+1]
    full_vec = np.transpose(np.hstack((np.hstack((pos_vec,contact_vec)),force_vec)))
    
    # Build filter array out of diagonal sub-matrices
    kp_arr = w_p*np.identity(3)
    kc_arr = w_c*np.identity(3)
    kf_arr = w_f*np.identity(3)
    filter_array = np.hstack((np.hstack((kp_arr,kc_arr)),kf_arr))
    
    # Take dot product of filter and full vector of pwm values
    final_pwm_vec = np.dot(filter_array,full_vec)
    
    # Debugging print of resultant finger pwms
    # print("Finger " + str(fing_num) + " pwm values after filter: " + str(final_pwm_vec))
    
    # Set cur_pwm_array values to result of filtering operation
    cur_pwm_array[prox_index:hype_index+1] = final_pwm_vec
#    print("filtPWMs: " + str(cur_pwm_array))


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
    rospy.Subscriber("finger_tendon_sensors", tendon_sns, tendon_sns_callback)
    rospy.Subscriber("finger_joint_sensors", joint_sns, joint_sns_callback)
    rospy.Subscriber("Sensor_Indiv", Sensor_Indiv, nib_sns_callback)
    
    
    
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
            # Get access to global state weights
#            global w_p, w_c, w_f
            w_p, w_c, w_f = 1, 0, 0
            
            grasp_substate = NOT_GRASPING

            # Define desired position values for testing
            des_prox_value = -300
            des_dist_value = -200
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
            position_control(des_prox_value, des_dist_value, 1)
            position_control(des_prox_value, des_dist_value, 2)
                        
            # Apply the new gain filter idea to set cur_pwm_array
            gain_filter(0)
            gain_filter(1)
            gain_filter(2)
            
            # Modify based on tendon tension
#            tendon_tension_control(1)
            
            # Cap final pwm value 
            final_pwm_cap(30);
        
        elif (state == MOVE_TO_POSE_2):
            # Define desired position values for testing
            des_prox_value = 100
            des_dist_value = -50
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
            position_control(des_prox_value, des_dist_value, 1)
            position_control(des_prox_value, des_dist_value, 2)
                        
            # Apply the new gain filter idea to set cur_pwm_array
            gain_filter(0)
            gain_filter(1)
            gain_filter(2)
            
            # TODO: modify based on tendon tension
#            tendon_tension_control(1)
           
            # Cap final pwm value 
            final_pwm_cap(40);
        
        elif (state == MOVE_TO_POSE_3):
            # Define desired position values for testing
            des_prox_value = 500
            des_dist_value = 500
            
            # Run proportional control on the des and sensed pos values
            position_control(des_prox_value, des_dist_value, 0)
            position_control(des_prox_value, des_dist_value, 1)
            position_control(des_prox_value, des_dist_value, 2)
                        
            # Apply the new gain filter idea to set cur_pwm_array
            gain_filter(0)
            gain_filter(1)
            gain_filter(2)
            
            # Modify based on tendon tension
#            tendon_tension_control(1)
           
            # Cap final pwm value 
            final_pwm_cap(40);   
       
        elif (state == PURE_CONTACT_CONTROL):
                        
            if (grasp_substate == NOT_GRASPING):
                grasp_substate = GRASP_START
                grasp_start_time = rospy.get_time()
                
            if (rospy.get_time() > grasp_start_time + 2.0):
                grasp_substate = GRASP_LATER
            
            # Get access to global state weights
#            global w_p, w_c, w_f
            w_p, w_c, w_f = 0, 0.5, 0.5
            
            # Call contact controller
            contact_control(0, 0) # des_xc, fing_num
            contact_control(0, 1) # des_xc, fing_num
            contact_control(0, 2) # des_xc, fing_num
            
            # Call grasp force controller
            grasp_force_control(0, 0) # des force, fing_num
            grasp_force_control(0, 1) # des force, fing_num
            grasp_force_control(0, 2) # des force, fing_num
            
            # Apply the new gain filter idea to set cur_pwm_array
            gain_filter(0)
            gain_filter(1)
            gain_filter(2)
            
            # Modify based on tendon tension
#            tendon_tension_control(1)
           
            # Cap final pwm value 
            final_pwm_cap(30);   
        
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
        # print("PWM Array: " + str(cur_pwm_array))
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