#!/usr/bin/env python3

import rospy
import roslaunch
import rospkg
from pathlib import Path

node_name = "ex3_map_saver"

rospy.init_node(node_name)
rate = rospy.Rate(1/5) # one cycle per 5 seconds

pkg_path = rospkg.RosPack().get_path('amr31001')
map_path = Path(pkg_path).joinpath("maps")
map_path.mkdir(exist_ok=True)
map_file = map_path.joinpath('my_map')

rl = roslaunch.scriptapi.ROSLaunch()
rl.start()

time = rospy.get_time()
while (rospy.get_time() - time) < 5:
    continue
rospy.loginfo(f"{node_name}: Initialised.")

while not rospy.is_shutdown():

    rospy.loginfo(f"Saving map to: '{map_file}'")

    rl.launch(
        roslaunch.core.Node(
            package="map_server",
            node_type="map_saver",
            args=f"-f {map_file}"
        )
    )
    
    try:
        rate.sleep()
    except rospy.ROSInterruptException:
        pass