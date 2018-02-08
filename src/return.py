import rospy
import math
import time
from kobuki_project.msg import Status
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import atexit



publisher_velocity = rospy.Publisher('kobuki_velocity', Twist, queue_size=1)
#publisher_velocity = rospy.Publisher('mobile_base/commands/velocity', Twist, queue_size=1)
forward = Twist(Vector3(0.2,0,0),Vector3(0,0,0))
backward = Twist(Vector3(-0.2,0,0),Vector3(0,0,0))
backward_obst = Twist(Vector3(-0.1,0,0),Vector3(0,0,0))
right_spin = Twist(Vector3(0,0,0),Vector3(0,0,-1.5))
left_spin = Twist(Vector3(0,0,0),Vector3(0,0,1.5))

ninety_left = Twist(Vector3(0,0,0),Vector3(0,0,3.14))
ninety_right = Twist(Vector3(0,0,0),Vector3(0,0,-3.14))
 

def retrieve_info():
	#haha
