#!/usr/bin/env python3
import rospy
import actionlib
import random
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time
from datetime import datetime
import subprocess
import os


class RandomExplorer:
    def __init__(self):
        rospy.init_node('random_explorer', anonymous=True)

        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        self.client.wait_for_server()

        self.last_position = None
        self.positon_check_interval = rospy.Duration(10)
        self.last_position_check_time = rospy.Time.now()
        self.min_distance_progress = 0.05


        # self.odom_sub = rospy.Subscriber("odom", Odometry, self.odom_callback)
        # self.current_x_velocity = 0.0

        self.exploration_time = 90  # seconds
        self.start_time = time.time()

        rospy.on_shutdown(self.stop_exploration)

    def send_random_goal(self):
        rospy.loginfo(f"In the send_random_goal function state : {self.client.simple_state}")
        if time.time() - self.start_time < self.exploration_time:
            random_x = random.uniform(-1.9, 1.9)
            random_y = random.uniform(-1.9, 1.9)
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = random_x
            goal.target_pose.pose.position.y = random_y
            goal.target_pose.pose.position.z = 0.0
            goal.target_pose.pose.orientation.x = 0.0
            goal.target_pose.pose.orientation.y = 0.0
            goal.target_pose.pose.orientation.z = 0.0
            goal.target_pose.pose.orientation.w = 1.0
            rospy.loginfo(f"Sending new random goal: x={random_x}, y={random_y}")
            self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)

    def active_cb(self):
        rospy.loginfo("Goal is now being processed by the Action Server")

    def feedback_cb(self, feedback):
        if time.time() - self.start_time >= self.exploration_time:
            rospy.loginfo("Exploration time ended in feedback_cb")
            self.stop_exploration()
            rospy.sleep(1)
        current_position = feedback.base_position.pose.position
        current_time = rospy.Time.now()
        if self.last_position is not None:
            if (current_time - self.last_position_check_time) > self.positon_check_interval:
                distance = self.cal_distance(current_position, self.last_position)
                if distance < self.min_distance_progress:
                    rospy.loginfo(f"distance = {distance} , current_position = {current_position} , self.last_position = {self.last_position}")
                    rospy.loginfo("Robot has not made significant progress, cancelling goal.")
                    self.client.cancel_goal()
                self.last_position_check_time = current_time
        self.last_position = current_position

    def cal_distance(self, pos1, pos2):
        return ((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2) ** 0.5

    def done_cb(self, status, result):
        rospy.loginfo(f"Goal completed with status: {status}")
        if status in [2,3,8,4]:
            rospy.loginfo(f"Time after completed goal: {time.time() - self.start_time}")
        elif status in [5]:
            rospy.loginfo("Goal failed or was rejected, stopping exploration.")
            self.stop_exploration()

    def stop_exploration(self):
        rospy.loginfo("In stop_exploration:::")
        rospy.loginfo(f"Final Time : {time.time() - self.start_time}")
        stop = Twist()  # Zero velocity to stop the robot
        self.cmd_vel_pub.publish(stop)
        self.client.cancel_all_goals()
        self.save_map()
        rospy.signal_shutdown("Stopping the robot.")

    # def odom_callback(self, msg):
    #     self.current_x_velocity = msg.twist.twist.linear.x
    #     rospy.loginfo(f"current_x_velocity: {self.current_x_velocity}")

    def save_map(self):
        map_directory = "/home/student/catkin_ws/src/auto_nav/maps/"
        map_filename = f'auto_map{datetime.now().strftime("%Y%m%d-%H%M%S")}'  # Customize the file name as needed

        # Ensure the directory exists
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)

        # Full path for map saving
        full_path = os.path.join(map_directory, map_filename)
        command = ["rosrun", "map_server", "map_saver", "-f", full_path]

        # Call the command using subprocess
        try:
            subprocess.check_call(command)
            rospy.loginfo("Map saved successfully at {}".format(full_path))
        except subprocess.CalledProcessError as e:
            rospy.logerr("Failed to save map: {}".format(str(e)))

    def explore(self):
        rospy.loginfo("Exploration starting ......")
        while not rospy.is_shutdown() and ((time.time() - self.start_time) < self.exploration_time):
            self.send_random_goal()
            print("While wait for the result")
            if not self.client.wait_for_result(rospy.Duration(25)):
                self.client.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            rospy.sleep(1)
        # self.stop_exploration()

if __name__ == '__main__':
    try:
        explorer = RandomExplorer()
        explorer.explore()
        # explorer.stop_exploration()
        # rospy.spin()  # Keep the node running while callbacks handle the navigation
    except rospy.ROSInterruptException:
        rospy.loginfo("ROSInterruptException")

