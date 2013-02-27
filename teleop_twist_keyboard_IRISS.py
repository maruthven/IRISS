#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
from rospy import timer

from geometry_msgs.msg import Twist
import subprocess
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

def keyNoBlock():
	tty.setcbreak(sys.stdin.fileno())
	select.select([sys.stdin],[], [], 1)
	#if(s == sys.stdin):
	#	global globalKey = sys.stdin.read(1)
	#	return true
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

	return key

speed = .5
turn = 0.05
globalKey = '['

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('teleop_twist_keyboard_IRISS')

	x = 0
	th = 0
	status = 14
	key = '['
	time = rospy.get_rostime()
	print rospy.get_rostime()
	random = 0

	try:
		print msg
		print vels(speed, turn)
		while(key != '\x03'):
			while(key != '=' and key != '\x03'):
				key = getKey()
				print "Input Recieved: "+key
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

#			time=time.time()
			speed=.10
			turn=.05
			time = 0
			#random = 0
			#time = rospy.get_rostime()
			newtime = time
			print "beginning loop"
			#while(key != '-' and key != '\x03'):
			while(time < 80 and key != '\x03'):
			#	print msg
				if (key == '\x03'):
					break
				else:
					print "turn "+i
					twist = Twist()
					twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
					twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn
					pub.publish(twist)
					timer.sleep(.8)
					time = time +1
					#newtime = rospy.get_rostime()	
				
			print "loop ended"

			twist = Twist()
			twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
			pub.publish(twist)
			print "Finished first round"
			if (key == '\x03'):
				break
			else:
				key = ' '
			
	#	SLEEP(5)
	#	wait(3000)#Assuming we can find a function that waits for 1 ms interval

	except:
		print random
		print time
		print e
		

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


