#!/usr/bin/env python3

import rospy
import waffle
from math import sqrt

node_name = "odom_based_navigation"

movement = "turn" # "move_fwd"
transition = True

rospy.init_node(node_name, anonymous=True)
rate = rospy.Rate(10) # hz
rospy.loginfo(f"{node_name}: Initialised.")

motion = waffle.Motion()
pose = waffle.Pose()

while not rospy.is_shutdown():

    pose.print()
    if transition:
        motion.stop()
        yaw_ref = pose.yaw
        xpos_ref = pose.posx
        ypos_ref = pose.posy
        current_yaw = 0.0
        current_distance = 0.0
        transition = False
        print(f"Entering state: {movement}")
    elif movement == "turn":
        # turn by 90 degrees
        current_yaw = current_yaw + abs(pose.yaw - yaw_ref)
        yaw_ref = pose.yaw
        if current_yaw > 90:
            movement = "move_fwd"
            transition = True
        else:
            motion.move_at_velocity(linear=0, angular=0.2)
    elif movement == "move_fwd":
        current_distance = current_distance+abs(sqrt(((pose.posx-xpos_ref)**2)+((pose.posy-ypos_ref)**2)))
        xpos_ref = pose.posx
        ypos_ref = pose.posy
        # add some code here!    
        if current_distance > 0.5:
            movement = "turn"
            transition = True 
        else:
            motion.move_at_velocity(linear=0.5, angular=0)

    rate.sleep()
