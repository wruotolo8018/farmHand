#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String
import serial
import time
import numpy as np
from futek_data_logger.msg import futek_data
from futek_data_logger.msg import z_pos
from plotter import plotData

# state definitions
ACTIVE = 1
DEACTIVATED = 0
state = DEACTIVATED

PLOTTED = 0
UNPLOTTED = 1
plot_state = PLOTTED

# Msg data arrays to be filled out below
cur_futek_data = futek_data()

# Sensor calibration variables
low_vals = []
high_vals = []
calibrated_vals = [0,0]
num_sensors = 2

# Data Storage Variables
cur_data_vec = np.zeros((3,1))
cur_data_array = np.zeros((3,1))


# Accessory functions 
def arduino_map(val, inMin, inMax, outMin, outMax):
    return float((val-inMin)*(outMax-outMin)/(inMax-inMin)+outMin)
def get_calibration_values():
    global low_vals, high_vals
    low_vals = [459,465] 
    high_vals = [144,144] 
    
# Callback Functions 
# State callback is unused right now but can be used to turn sensor on and off
def state_callback(data):
    incomingString = str(data.data)
    global state, plot_state
    if (incomingString == 'engage_1'):
        state = ACTIVE
        print("Starting data collection!")
        global cur_data_array
        cur_data_array = np.zeros((2,1))
    elif(incomingString == 'end_data'):
        state = DEACTIVATED
        plot_state = UNPLOTTED
        print("Finishing data collection!")
        
def save_data(data):
    file_name = raw_input('File name to save: ')
    full_name = './saved_data/' + file_name + '.npy'
    with open(full_name, 'wb') as f:
        np.save(f, data)
        
def futek_data_callback(data):
    val_1 = data.futek1
    val_2 = data.futek2
    global cur_data_vec
    cur_data_vec[0,0] = val_1
    cur_data_vec[1,0] = val_2
    
def position_callback(data):
    val_3 = data.z_pos
    global cur_data_vec
    cur_data_vec[2,0] = val_3
    
# Main node
def data_processor():
    # Setup node
    rospy.init_node('data_processor', anonymous=True)
    
    # Setup subscription to state machine
    rospy.Subscriber("master_state", String, state_callback)
    rospy.Subscriber("futek_sensors", futek_data, futek_data_callback)
    rospy.Subscriber("ur5_position", z_pos, position_callback)
    
    # Set loop speed
    rate = rospy.Rate(30) #50 hz
    
    # Set calibration values
    get_calibration_values()
    
    # Output that things are going
    print("Data processor node started")
    
    while not rospy.is_shutdown():  
        if state == ACTIVE:
                            
                # Append new data to np array
                global cur_data_array, cur_data_vec
                print(cur_data_array.shape)
                print(cur_data_vec.shape)
                cur_data_array = np.hstack((cur_data_array, cur_data_vec))
                print(cur_data_array.shape)
                
            
        elif state == DEACTIVATED:
            # Plot current data set to see if it's reasonable
            global plot_state
            if (plot_state == UNPLOTTED):
                global cur_data_array
                plotData(cur_data_array)
                plot_state = PLOTTED
                
                save_data(cur_data_array)
                print("Data Saved")
        
        # Sleep to set read rate based on desired value
        rate.sleep()

if __name__ == '__main__':
    try:
        # Setup serial connection
        com = serial.Serial('/dev/ttyACM0',baudrate=115200)
        time.sleep(0.5) # Not sure this is necessary but seems to stabilize comms some
        
        # Start controller node
        data_processor()
        
    except rospy.ROSInterruptException:
        pass
    
