#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class LidarReader:
    def __init__(self):
        rospy.init_node('lidar_reader', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.ctrl_c = False
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.scan_data = None
        rospy.on_shutdown(self.shutdownhook)

    def shutdownhook(self):
        self.ctrl_c = True

    def laser_callback(self, data):
        self.scan_data = data

    def rotate_and_avg(self, angular_speed):
        vel_cmd = Twist()
        vel_cmd.angular.z = angular_speed
        while self.scan_data is None and not self.ctrl_c:
            rospy.sleep(0.1)  # Wait for LiDAR data
        if self.ctrl_c:
            return
        angle_increment = self.scan_data.angle_increment
        num_readings = len(self.scan_data.ranges)
        num_avg_readings = 1  # Changed to 1 for 1-degree increments
        num_groups = int(num_readings / num_avg_readings)
        while not self.ctrl_c:
            averaged_ranges = []
            for group_index in range(num_groups):
                start_index = group_index * num_avg_readings
                end_index = (group_index + 1) * num_avg_readings
                group_ranges = self.scan_data.ranges[start_index:end_index]
                averaged_range = np.mean(group_ranges)
                averaged_ranges.append(averaged_range)
                if 0.85 <= averaged_range <= 0.9:
                    rospy.loginfo(f"Stopped at averaged range: {averaged_range}")
                    vel_cmd.angular.z = 0.0
                    self.pub.publish(vel_cmd)
                    return
            rospy.loginfo(f"Averaged ranges for 1 degree: {averaged_ranges}")
            self.pub.publish(vel_cmd)
            rospy.sleep(1)  # Rotate for 1 second

def main():
    lidar_reader = LidarReader()
    try:
        # Rotate slowly at 30 degrees per second
        lidar_reader.rotate_and_avg(0.323)  # angular_speed = 0.523 rad/s (about 30 degrees/s)
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
