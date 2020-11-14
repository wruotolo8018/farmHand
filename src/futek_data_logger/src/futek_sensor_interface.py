#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String
import serial
import time
import numpy as np
from futek_data_logger.msg import futek_data
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
cur_data_array = np.zeros((2,1))

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
    
# Main node
def futek_sensor_serial():
    # Setup node
    rospy.init_node('futek_sensor_serial', anonymous=True) #will need 
    
    # Setup subscription to state machine
    rospy.Subscriber("master_state", String, state_callback)
    
    # Setup publisher to flex sensor data topic
    global futek_sense_pub
    futek_sense_pub = rospy.Publisher('futek_sensors', futek_data, queue_size=10)
    
    # Set loop speed
    rate = rospy.Rate(50) #50 hz
    
    # Set calibration values
    get_calibration_values()
    
    # Output that things are going
    print("Basic futek sensor read & publish")
    
    while not rospy.is_shutdown():  
        if state == ACTIVE:
            # Read serial interface for current data
            read_string = com.read_until()
            
            # Print currently read string for debugging
            print(read_string)
            
            # Populate message fields appropriately
            split_read_string = read_string.split('_')
            
            # Catch partially sent message errors by ensuring length
            # +2 for time field and extra value after last underscore
            if (len(split_read_string) == num_sensors+2): 
                global low_vals, high_vals
                
                # Iterate through sensor values and calibrate to standardized range
                for i in range(num_sensors):
                    
                    # Get current value for calibration
                    val = int(split_read_string[i])
                    
                    # TODO: Catch divide by zero error
#    
                    # Map value to standardized range (other controllers assume 0-1023)
                    calibrated_vals[i] = arduino_map(val, low_vals[i], high_vals[i], 0.0, 15.0)
                 
                # Print calibrated values for debugging purposes
                print("Calibrated vals: " + str(calibrated_vals))
                
                # Fill out flex data msg type with calibrated values
                cur_futek_data.futek1 = calibrated_vals[0]
                cur_futek_data.futek2 = calibrated_vals[1]
                
                # publish sensor data
                futek_sense_pub.publish(cur_futek_data)
                
                # Append new data to np array
                new_data_vec = np.zeros((2,1))
                new_data_vec[0,0] = calibrated_vals[0]
                new_data_vec[1,0] = calibrated_vals[1]
                global cur_data_array
                cur_data_array = np.hstack((cur_data_array, new_data_vec))
                print(cur_data_array.shape)
                
            
        elif state == DEACTIVATED:
            read_string = com.read_until()
            # Save Accumulated Data to File
            dummyVar = 0
            
            # Plot current data set to see if it's reasonable
            global plot_state
            if (plot_state == UNPLOTTED):
                global cur_data_array
                plotData(cur_data_array)
                plot_state = PLOTTED
        
        # Sleep to set read rate based on desired value
        rate.sleep()

if __name__ == '__main__':
    try:
        # Setup serial connection
        com = serial.Serial('/dev/ttyACM0',baudrate=115200)
        time.sleep(0.5) # Not sure this is necessary but seems to stabilize comms some
        
        # Start controller node
        futek_sensor_serial()
        
    except rospy.ROSInterruptException:
        pass
    