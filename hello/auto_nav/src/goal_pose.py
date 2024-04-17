#!/usr/bin/env python3

# import rospy
# import actionlib
# from geometry_msgs.msg import Twist
# from sensor_msgs.msg import LaserScan
# import random
# import time

# class ExplorerBot:
#     def __init__(self):
#         rospy.init_node('explorer_bot', anonymous=True)

#         self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
#         rospy.Subscriber('/scan', LaserScan, self.scan_callback)

#         self.obstacle_in_front = False
#         self.exploration_time = 10  # seconds

#     def scan_callback(self, msg):
#         # Enhance obstacle detection by considering a wider range
#         front_ranges = msg.ranges[:len(msg.ranges)//16] + msg.ranges[-len(msg.ranges)//16:]
#         side_ranges = msg.ranges[len(msg.ranges)//4:-len(msg.ranges)//4]
#         self.obstacle_in_front = min(front_ranges) < 0.5
#         self.space_on_sides = min(side_ranges) > 0.5  # Check if there's more space on the sides

#     def explore(self):
#         start_time = time.time()
#         rate = rospy.Rate(10)  # 10Hz
#         twist = Twist()

#         while not rospy.is_shutdown() and time.time() - start_time < self.exploration_time:
#             if self.obstacle_in_front:
#                 twist.linear.x = 0.0
#                 # Instead of randomly turning, check where more space is available
#                 if self.space_on_sides:
#                     # try to find which angle that it is has lower obstacles (higher value in the range)
#                     # convert this the index of that range to the angle that it should go
#                     # Then use the twist.angular.z (rad/s) to turn the robot around 
#                     TODO
#             else:
#                 twist.linear.x = 0.2
#                 twist.angular.z = 0.0

#             self.vel_pub.publish(twist)
#             rate.sleep()

#         self.vel_pub.publish(Twist())
#         rospy.loginfo("Exploration finished.")

# if __name__ == '__main__':
#     try:
#         explorer_bot = ExplorerBot()
#         explorer_bot.explore()
#     except rospy.ROSInterruptException:
#         pass


import rospy
import actionlib
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random
import time

class ExplorerBot:
    def __init__(self):
        rospy.init_node('explorer_bot', anonymous=True)

        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.obstacle_in_front = False
        self.exploration_time = 90  # seconds

    def scan_callback(self, msg):
        # Enhance obstacle detection by considering a wider range
        front_ranges = msg.ranges[:len(msg.ranges)//16] + msg.ranges[-len(msg.ranges)//16:]
        side_ranges = msg.ranges[len(msg.ranges)//4:-len(msg.ranges)//4]
        self.obstacle_in_front = min(front_ranges) < 0.4
        self.space_on_sides = min(side_ranges) > 0.1  # Check if there's more space on the sides

    def explore(self):
        start_time = time.time()
        rate = rospy.Rate(10)  # 10Hz
        twist = Twist()

        while not rospy.is_shutdown() and time.time() - start_time < self.exploration_time:
            if self.obstacle_in_front:
                twist.linear.x = 0.0
                # Instead of randomly turning, check where more space is available
                if self.space_on_sides:
                    twist.angular.z = random.choice([-0.5, 0.5])  # Adjust angular speed for smoother turn
                else:
                    twist.angular.z = random.choice([-1.0, 1.0])
            else:
                twist.linear.x = 0.2
                twist.angular.z = 0.0

            self.vel_pub.publish(twist)
            rate.sleep()

        self.vel_pub.publish(Twist())
        rospy.loginfo("Exploration finished.")

if __name__ == '__main__':
    try:
        explorer_bot = ExplorerBot()
        explorer_bot.explore()
    except rospy.ROSInterruptException:
        pass