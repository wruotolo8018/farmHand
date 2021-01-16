#!/usr/bin/env python
# license removed for brevity

# Imports
import rospy
from std_msgs.msg import String

# Setup global variables
state_string = "manual_input"

def master_state_machine():
    
    # Set up publisher to master_state topic
    pub_master_state = rospy.Publisher('master_state', String, queue_size=10)
    
    # State node at 10hz (speed should be flexible)
    rospy.init_node('master_state_machine', anonymous=True)
#    rate = rospy.Rate(10) # 10hz
    
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
        input_string = raw_input('Input: ')
        
        # Handle input and publish appropriate state
        if (input_string == ' '):
            state_string = "stop"
            pub_master_state.publish(state_string)
        elif (input_string == '1'):
            state_string = "move_to_pose_1"
            pub_master_state.publish(state_string)
        elif (input_string == '2'):
            state_string = "pregrasp_wide"
            pub_master_state.publish(state_string)
        elif (input_string == '3'):
            state_string = "grasp_pinch"
            pub_master_state.publish(state_string)
        elif (input_string == '4'):
            state_string = "tighten"
            pub_master_state.publish(state_string)
        elif (input_string == '5'):
            state_string = "loosen"
            pub_master_state.publish(state_string)
        elif (input_string == '6'):
            raw_input("Go to home? Press Enter")
            state_string = "home_arm"
            pub_master_state.publish(state_string)

            raw_input("Pregrasp?")
            print("Pregrasping")
            state_string = "pregrasp_wide"
            pub_master_state.publish(state_string)

            raw_input("Start trial? Press Enter")
            state_string = "start"
            pub_master_state.publish(state_string)

            raw_input("Go to position 1? Press Enter")
            print("Performing displacement 1")
            state_string = "move_1"
            pub_master_state.publish(state_string)

            raw_input("Go to position 2? Press Enter")
            print("Going to position 2 and grasping")
            state_string = "move_2"
            pub_master_state.publish(state_string)

            raw_input("Start grasping? Press Enter")
            state_string = "grasp_wide"
            pub_master_state.publish(state_string)

            # raw_input("Grasp object?")
            # print("Grasping")
            # state_string = "grasp_wide"
            # pub_master_state.publish(state_string)

            raw_input("Go to position 3? Press Enter")
            print("Going to position 3")
            state_string = "move_3"
            pub_master_state.publish(state_string)

            raw_input("Go to home? Press Enter")
            state_string = "home_fingers"
            pub_master_state.publish(state_string)
            state_string = "home_arm"
            pub_master_state.publish(state_string)




            # raw_input("Grasp object?")
            # print("Grasping")
            # state_string = "grasp_pinch"
            # pub_master_state.publish(state_string)
            # # rospy.sleep(2.0)
            #
            # raw_input("Go to position 3? Press Enter")
            # print("Going to position 3")
            # state_string = "move_3"
            # pub_master_state.publish(state_string)
            # # rospy.sleep(4.0)
            #
            # raw_input("Grasp object?")
            # print("Grasping")
            # state_string = "grasp_pinch"
            # pub_master_state.publish(state_string)
            # # rospy.sleep(2.0)
            #
            # raw_input("Go to position 4? Press Enter")
            # print("Going to position 4")
            # state_string = "move_4"
            # pub_master_state.publish(state_string)
            # # rospy.sleep(4.0)
            #
            # raw_input("Go to position 5? Press Enter")
            # print("Going to position 5")
            # state_string = "move_5"
            # pub_master_state.publish(state_string)
            # # rospy.sleep(4.0)


if __name__ == '__main__':
    try:
        master_state_machine()
    except rospy.ROSInterruptException:
        pass