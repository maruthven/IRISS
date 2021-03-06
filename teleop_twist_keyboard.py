#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist
import time

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
anything else : stop

CTRL-C to quit
"""

moveBindings = {
		'i':(1,0),
		'o':(1,-1),
		'j':(0,1),
		'l':(0,-1),
		'u':(1,1),
		',':(-1,0),
		'.':(-1,1),
		'm':(-1,-1),
	       }

speedBindings={
		'q':(1.1,1.1),
		'z':(.9,.9),
		'w':(1.1,1),
		'x':(.9,1),
		'e':(1,1.1),
		'c':(1,.9),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

speed = .5
turn = 0.05

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('teleop_twist_keyboard_IRISS')

	x = 0
	th = 0
	status = 0
	key = '['
	#time = time.time()
	#print time

	try:
		while(1):
			while(key != '='):
				key = getKey()
				print "Input Recieved"
				if key in moveBindings.keys():
					x = moveBindings[key][0]
					th = moveBindings[key][1]
				elif key in speedBindings.keys():
					speed = speed * speedBindings[key][0]
					turn = turn * speedBindings[key][1]

					print vels(speed,turn)
					if (status == 14):
						print msg
						status = (status + 1) % 15
					else:
						x = 0
						th = 0
						if (key == '\x03'):
							break

						twist = Twist()
						twist.linear.x = x*speed; twist.linear.y = 0; twist.linear.z = 0
						twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
						pub.publish(twist)
			print "Starting Sequence"
			time = time.time()
			print "Error in Time"
			speed=.10
			turn=.05
			print "Starting while loop"
			while(time + 5.0 > time()):
				print msg
				print vels(speed,turn)
				twist = Twist()
				twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
				twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn
				pub.publish(twist)
				time.sleep(.5)
			
	#	SLEEP(5)
	#	wait(3000)#Assuming we can find a function that waits for 1 ms interval

	except:
		print "Error Recieved", sys.exc_info()[0]

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


