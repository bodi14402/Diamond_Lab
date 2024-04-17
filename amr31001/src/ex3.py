#!/usr/bin/env python3

import rospy
import waffle

node_name = "wall_follower"

rospy.init_node(node_name, anonymous=True)
rate = rospy.Rate(2) # hz
rospy.loginfo(f"{node_name}: Initialised.")

motion = waffle.Motion()
lidar = waffle.Lidar()

lin_vel = 0.0
ang_vel = 0.0
movement = ""

while not rospy.is_shutdown():

    lin_vel = 0.1

    wall_rate = lidar.distance.l3 - lidar.distance.l4
    front_distance = lidar.distance.front
    print(lidar.distance)

    if abs(wall_rate) < 0.001:
        movement = "go straight"
        ang_vel = 0.0
    elif wall_rate > 0:
        movement = "turn left"
        ang_vel = 0.2
    elif wall_rate < 0:
        movement = "turn right"
        ang_vel = -0.2
    elif front_distance < 0.2:
        movement = "stop and turn"
        motion.move_at_velocity(linear=0, angular=0.2)
    

    
    print(f"{wall_rate=:.3f}")
    print(f"{movement=}\n")
    motion.move_at_velocity(linear=lin_vel, angular=ang_vel)
    rate.sleep()
    