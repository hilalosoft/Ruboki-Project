#!/usr/bin/env python
import rospy
from kobuki_project.msg import Status
from Tkinter import *

root = Tk()

def draw(status):
	x = -1*status.x*150 + 500
	y = status.y*150 + 500 
	if status.left or status.front or status.right :
		canvas.create_oval(x,y,x +20 ,y+20, fill = "orange")
	canvas.create_oval(x,y,x+1 ,y+1, fill = "red")

canvas = Canvas(root, width=1000, height=1000)
canvas.pack()
rospy.init_node('monitor')
rospy.Subscriber("/kobuki_status", Status, draw)




root.mainloop()




	