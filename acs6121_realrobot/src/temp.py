#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

class LidarReader:
    def __init__(self):
        self.readings = {}  # Store the last 7 range readings for each degree
        self.averages = []  # Store the average readings for each 5-degree interval
        self.subscriber = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
    
    def laser_callback(self, data):
        averages = []  # Temporary list to store averages for each 5-degree interval
        # Iterate through each degree from 0 to 360 with a 5-degree interval
        for degree in range(0, 361, 5):
            # Calculate the indices corresponding to the current 5-degree interval
            start_index = int(degree / data.angle_increment)
            end_index = int((degree + 5) / data.angle_increment)
            # Store the range readings for the current 5-degree interval
            self.readings[degree] = data.ranges[start_index:end_index]
            # Check if there are readings for the current 5-degree interval
            if self.readings[degree]:
                # Calculate the average of the range readings for the current 5-degree interval
                avg_reading = sum(self.readings[degree]) / len(self.readings[degree])
                averages.append(avg_reading)  # Apped the average to the temporary list
        self.averages = averages  # Update the averages list with the temporary list

def main():
    rospy.init_node('lidar_reader', anonymous=True)
    lidar_reader = LidarReader()
    rospy.spin()  # Keep the node running
    print("Array of average readings:", lidar_reader.averages)
    num_values = len(lidar_reader.averages)
    print("Number of values in the array:", num_values)

if __name__ == '__main__':
    main()
