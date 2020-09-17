#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import serial
import time

cur_motor_string = ""

def motor_cmd_callback(data):
    global cur_motor_string
    cur_motor_string = str(data.data)

def motor_talker():
    
    # Setup subscription to cmd_motor_controller topic
    rospy.Subscriber("motor_cmd", String, motor_cmd_callback)
    rospy.init_node('finger_serial_interface', anonymous=True)
    rate = rospy.Rate(20) # 10hz was used before and def stable
    print("Motor serial interface initialized")
    
    # Constantly update output motor string based on incoming commands
    global cur_motor_string
    while not rospy.is_shutdown():
#        print(cur_motor_string)
        com.write(cur_motor_string)
        rate.sleep()

if __name__ == '__main__':
    try:
        # Setup serial connection
        com = serial.Serial('/dev/ttyACM1',baudrate=115200)
        time.sleep(0.5) # Not sure this is necessary but seems to stabilize comms some
        motor_talker()
        
    except rospy.ROSInterruptException:
        pass