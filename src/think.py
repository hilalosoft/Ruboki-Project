#!/usr/bin/env python

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

goback = False
goleft = False
goright = False
goforward = False
right90 = False
left90 = False
turn = ""
last_obstacle = []
turn_right = False
turn_left = False
bumped = False

arrived_base=False
return_base=False
inv_command_history = []
returnstep = 30

obstacles = []

def exit_handler():
	out_file = open("map.txt","w")
	for obstacle in obstacles:
		obst = "{}".format(obstacle[0])+","+"{}".format(obstacle[1])+"\n"
		out_file.write(obst)
	out_file.close()



def distance(x1, y1, x2, y2):
	xd = x1 - x2
	yd = y1 - y2
	return math.sqrt(xd * xd + yd * yd)

def decide(status):

	#print status.x
	#print status.y
	#print status.left
	#print status.front
	#print status.right
	global goback
	global goleft
	global goright
	global left90
	global right90
	global goforward
	global last_obstacle
	global backward_obst
	global turn
	global turn_right
	global turn_left
	global bumped
	
	global arrived_base
	global return_base
	global inv_command_history
	global returnstep
	#dist = 0.0

	
	if not inv_command_history == [] and (len(inv_command_history)>returnstep and returnstep>=0) or return_base:
		if returnstep>0:
			return_base=True
		#readfile=open("position.txt","r")
		#readfile.seek(numchar[len(numchar)-1])
		#s=readfile.readline()
		print(inv_command_history[returnstep] + "    " + str(returnstep))
		current = inv_command_history[returnstep]
		goforward = False
		goback = False
		goleft = False
		goright = False
		right90 = False
		left90 = False
		turn_left = False
		turn_right = False
		if(current == "goforward"):
			goforward = True
		elif(current == "goback"):
			goback = True
		elif(current == "goleft"):
			goleft = True
		elif(current == "goright"):
			goright = True
		elif(current == "right90"):
			right90=True
		elif(current == "left90"):
			left90 == True
		elif(current == "turn_left"):
			turn_left = True
		elif(current == "turn_right"):
			turn_right = True
		




		returnstep=returnstep-1
		if returnstep<0:
			return_base = False

	elif len(inv_command_history)>returnstep or returnstep < 0 or arrived_base:
		if(not arrived_base):
			print("returned to base!")
			return_base=False
			arrived_base=True
		return
	
	if not return_base and not last_obstacle == [] and distance(status.x, status.y, last_obstacle[0], last_obstacle[1]) < 0.3:
		dist = distance(status.x, status.y, last_obstacle[0], last_obstacle[1])
		if dist > 0.2 and not goforward:
			if turn == "left":
				turn_left = True
			else:
				turn_right = True
			goback = False
	else:		
		goforward = False


	if not bumped and not return_base:

		for obstacle in obstacles:
			dist = distance(status.x, status.y, obstacle[0], obstacle[1])
			if dist < 0.3:
				print "Vecchio ostacolo"
				last_obstacle = (obstacle[0], obstacle[1])
				bumped = True
				return

		
	

	if not return_base and (status.left or status.front or status.right) :
		last_obstacle = (status.x, status.y)
		obstacles.append((status.x, status.y))
		goback = True
		#print("Ostacolo aggiunto")
		if status.left:
			turn = "right"
		elif status.right:
			turn = "left"
		else:
			turn = "right"
		goforward = False

	if turn_right:
		print "Esco a destra"
		publisher_velocity.publish(right_spin)
		time.sleep(1.5)
		inv_command_history.append("goleft")
		turn_right = False
		goforward = True
		

	if turn_left:
		print "Esco a sinistra"
		publisher_velocity.publish(left_spin)
		time.sleep(1.5)
		inv_command_history.append("goright")
		turn_left = False
		goforward = True

	if goback:
		print "Indietro\n"
		publisher_velocity.publish(backward)
		inv_command_history.append("goforward")
		return
	
	if left90:
		print "90 left"
		publisher_velocity.publish(ninety_left)
		time.sleep(1.2)
		left90 = False
		inv_command_history.append("right90")
		return

	if right90:
		print "90 right"
		publisher_velocity.publish(ninety_right)
		time.sleep(1.2)
		right90 = False
		inv_command_history.append("left90")
		return

	if goleft:
		print "left"
		publisher_velocity.publish(left_spin)
		time.sleep(1.5)
		goleft = False
		inv_command_history.append("goright")
		return

	if goright:
		print "right"
		publisher_velocity.publish(right_spin)
		time.sleep(1.5)
		goright = False
		inv_command_history.append("goleft")
		return

	if goforward:
		print "Mi allontano\n"
		publisher_velocity.publish(forward)
		inv_command_history.append("goback")
		return

	publisher_velocity.publish(forward)
	inv_command_history.append("goback")
	turn_right = False
	turn_left = False
	goback = False
	goforward = False
	bumped = False
	turn = ""
	print "Avanti"
	


def think():
	rospy.init_node('think')
	rospy.Subscriber("/kobuki_status", Status, decide)
	atexit.register(exit_handler)
	rospy.spin()


if __name__ == '__main__':
	try:
		think()
	except rospy.ROSInterruptException:
		pass
