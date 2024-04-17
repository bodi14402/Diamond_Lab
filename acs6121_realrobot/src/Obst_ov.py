#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower:
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        self.twist = Twist()

    def callback(self, msg):
        # Assuming the sensor provides data for the first 15 degrees on the right and left
        right = min(min(msg.ranges[0:15]), 10)
        left = min(min(msg.ranges[-15:]), 10)

        if right < 0.7:  # If the wall is detected within 0.7m on the right
            self.twist.linear.x = 0  # Move forward
            self.twist.angular.z = -0.7  # Turn left
        elif left < 0.7:  # If the wall is detected within 0.7m on the left
            self.twist.linear.x = 0  # Move forward
            self.twist.angular.z = 0.7  # Turn right
        else:
            self.twist.linear.x = 0.5  # Move forward
            self.twist.angular.z = 0.0  # Stop turning

        self.pub.publish(self.twist)

if __name__ == '__main__':
    rospy.init_node('wall_follower')
    wall_follower = WallFollower()
    rospy.spin() 