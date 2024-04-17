#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

class LiDARListener:
    def __init__(self):
        rospy.init_node('lidar_listener', anonymous=True)
        rospy.Subscriber("/scan", LaserScan, self.lidar_callback)
        self.lidar_data = None
        self.waypoints = {}  # Dictionary to store waypoints for each angle
        self.goals = []

    def lidar_callback(self, data):
        self.lidar_data = data.ranges

    def get_distances(self):
        if self.lidar_data is not None:
            distances = {
                '0_degrees': self.lidar_data[0],
                '90_degrees': self.lidar_data[len(self.lidar_data) // 4],
                '180_degrees': self.lidar_data[len(self.lidar_data) // 2],
                '270_degrees': self.lidar_data[3 * len(self.lidar_data) // 4]
            }
            return distances
        else:
            return None

    def update_waypoints(self):
        if self.lidar_data is not None:
            angles = [0, np.pi / 2, np.pi, 3 * np.pi / 2]  # Angles in radians
            for angle in angles:
                index = int(angle / (2 * np.pi) * len(self.lidar_data))
                distance = self.lidar_data[index]
                x = distance * np.cos(angle)
                y = distance * np.sin(angle)
                self.waypoints[f"{int(np.degrees(angle))}_degrees"] = (x, y)

    def get_furthest_waypoint(self):
        max_distance = max(self.get_distances().values())
        furthest_angle = None
        for angle, distance in self.get_distances().items():
            if distance == max_distance:
                furthest_angle = angle
                break
        return self.waypoints.get(furthest_angle, None)

    def create_goals(self):
        furthest_waypoint = self.get_furthest_waypoint()
        if furthest_waypoint is not None:
            x, y = furthest_waypoint
            goal1 = (x - 0.25, 1.25)
            goal2 = (x - 0.25, -1.25)
            self.goals = [goal1, goal2]

def main():
    lidar_listener = LiDARListener()
    rospy.sleep(1)  # Wait for the subscriber to receive LiDAR data
    lidar_listener.update_waypoints()
    lidar_listener.create_goals()
    print("Goals created:")
    print(lidar_listener.goals)

if __name__ == '__main__':
    main()
