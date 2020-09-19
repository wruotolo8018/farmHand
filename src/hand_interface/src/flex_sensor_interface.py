#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String
import serial
import time
import numpy as np
from hand_interface.msg import flex_sns

# state definitions
ACTIVE = 1
DEACTIVATED = 0
state = ACTIVE

# Msg data arrays to be filled out below
cur_flex_data = flex_sns()

# Sensor calibration variables
low_vals = []
high_vals = []
calibrated_vals = [0,0,0,0,0,0]
num_sensors = 6

# Accessory functions 
def arduino_map(val, inMin, inMax, outMin, outMax):
    return int((val-inMin)*(outMax-outMin)/(inMax-inMin)+outMin)
def get_calibration_values():
    global low_vals, high_vals
    low_vals = [413,430,0,0,0,0] 
    high_vals = [190,210,1023,1023,1023,1023] 
    
# Callback Functions 
# State callback is unused right now but can be used to turn sensor on and off
def state_callback(data):
    incomingString = str(data.data)
    global state
    
# Main node
def basic_sensor_serial():
    # Setup node
    rospy.init_node('basic_sensor_serial', anonymous=True)
    
    # Setup subscription to state machine
    rospy.Subscriber("master_state", String, state_callback)
    
    # Setup publisher to flex sensor data topic
    global flex_sense_pub
    flex_sense_pub = rospy.Publisher('flex_sensors', flex_sns, queue_size=10)
    
    # Set loop speed
    rate = rospy.Rate(50) #50 hz
    
    # Set calibration values
    get_calibration_values()
    
    # Output that things are going
    print("Basic interface with finger sensors running.")
    
    while not rospy.is_shutdown():  
        if state == ACTIVE:
            # Read serial interface for current data
            read_string = com.read_until()
            
            # Print currently read string for debugging
            # print(read_string)
            
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
                    calibrated_vals[i] = arduino_map(val, low_vals[i], high_vals[i], 0, 1023)
                 
                # Print calibrated values for debugging purposes
                #print(calibrated_vals)
                #print(read_string)
                #print("Prox Tendon Val: " + str(calibrated_vals[3]))
                #print("Dist Tendon Val: " + str(calibrated_vals[4]))
                #print("Hype Tendon Val: " + str(calibrated_vals[5]))
                #print(" ")
                
                # Fill out flex data msg type with calibrated values
                cur_flex_data.prox1 = calibrated_vals[0]
                cur_flex_data.dist1 = calibrated_vals[1]
                cur_flex_data.prox2 = calibrated_vals[2]
                cur_flex_data.dist2 = calibrated_vals[3]
                cur_flex_data.prox3 = calibrated_vals[4]
                cur_flex_data.dist3 = calibrated_vals[5]
                
            # publish sensor data
            flex_sense_pub.publish(cur_flex_data)
            
        elif state == DEACTIVATED:
            # Do nothing
            dummyVar = 0
        
        # Sleep to set read rate based on desired value
        rate.sleep()

if __name__ == '__main__':
    try:
        # Setup serial connection
        com = serial.Serial('/dev/ttyACM0',baudrate=115200)
        time.sleep(0.5) # Not sure this is necessary but seems to stabilize comms some
        
        # Start controller node
        basic_sensor_serial()
        
    except rospy.ROSInterruptException:
        pass
    
