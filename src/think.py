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

numchar=[]

ninety_left = Twist(Vector3(0,0,0),Vector3(0,0,3.14))
ninety_right = Twist(Vector3(0,0,0),Vector3(0,0,-3.14))

movement = []


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
out=open("position.txt","w")
out.write(" ")
out.close()

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
	global count
	count =0
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

	#dist = 0.0


	if not last_obstacle == [] and distance(status.x, status.y, last_obstacle[0], last_obstacle[1]) < 0.3:
		dist = distance(status.x, status.y, last_obstacle[0], last_obstacle[1])
		if dist > 0.2 and not goforward:
			if turn == "left":
				turn_left = True
			else:
				turn_right = True
			goback = False
	else:
		goforward = False


	if not bumped:
		for obstacle in obstacles:
			dist = distance(status.x, status.y, obstacle[0], obstacle[1])
			if dist < 0.3:
				print("Vecchio ostacolo")
				last_obstacle = (obstacle[0], obstacle[1])
				bumped = True
				return
	


	#we write in the file all the information about the movement  the position and the desicion made
	if status.left or status.front or status.right :

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
		print("Esco a destra")
		publisher_velocity.publish(right_spin)
		time.sleep(1.5)
		turn_right = False
		goforward = True
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",rightspin")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",rightspin"+"\n")
		outfile.close()

	if turn_left:
		print("Esco a sinistra")
		publisher_velocity.publish(left_spin)
		time.sleep(1.5)
		turn_left = False
		goforward = True
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",leftspin")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",leftspin"+"\n")
		outfile.close()

	if goback:
		print("Indietro")
		publisher_velocity.publish(backward)
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",back")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",back"+"\n")
		outfile.close()
		return
	
	if left90:
		print("90 left")
		publisher_velocity.publish(ninety_left)
		time.sleep(1.2)
		left90 = False
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",left90")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",left90"+"\n")
		outfile.close()
		return

	if right90:
		print("90 right")
		publisher_velocity.publish(ninety_right)
		time.sleep(1.2)
		right90 = False
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",right90")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",right90"+"\n")
		outfile.close()
		return

	if goleft:
		print("left")
		publisher_velocity.publish(left_spin)
		time.sleep(1)
		goleft = False
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",goleft")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",goleft"+"\n")
		outfile.close()
		return

	if goright:
		print("right")
		publisher_velocity.publish(right_spin)
		time.sleep(1)
		goright = False
		outfile=open("postition.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",rightspin")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",rightspin"+"\n")
		outfile.close()
		return

	if goforward:
		print("Mi allontano\n")
		publisher_velocity.publish(forward)
		outfile=open("position.txt","a")
		count+=len(repr(status.x))+len(repr(status.y))+len(",forward")+len("\n")
		numchar.append(count)
		outfile.write(repr(status.x)+repr(status.y)+",forward"+"\n")
		outfile.close()
		return

	publisher_velocity.publish(forward)
	outfile=open("position.txt","a")
	count+=len(repr(status.x))+len(repr(status.y))+len(",forward")+len("\n")
	numchar.append(count)
	outfile.write(repr(status.x)+repr(status.y)+",forward"+"\n")
	outfile.close()
	turn_right = False
	turn_left = False
	goback = False
	goforward = False
	bumped = False
	turn = ""
	print("Avanti")
	


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
