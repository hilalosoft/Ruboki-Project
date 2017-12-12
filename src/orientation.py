#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry


def get_orientation(odometry):
	orientation = odometry.pose.pose.orientation.z
	print("ORIENTATION: {}\n".format(orientation))

def orientation():
	rospy.init_node('orientation')
	rospy.Subscriber("/odom", Odometry, get_orientation)
	rospy.spin()
	

if __name__ == '__main__':
	try:
		orientation()
	except rospy.ROSInterruptException:
		pass
