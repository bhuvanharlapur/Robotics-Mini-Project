#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Point,Twist
from goal_publisher.msg import PointArray
from gazebo_msgs.msg import ModelStates
from sensor_msgs.msg import LaserScan
import numpy as np
import time
import math
import ast
from tf.transformations import euler_from_quaternion
from math import atan2

angle_min= -1.57079637051
angle_max= 1.53938043118
angle_incr = 0.0314159281552
x=0.0
y=0.0
theta=0.0
goal_x=[]
goal_y=[]
goal_points=[0.0]*20
goal_1= [0]*3
goal_2= [0]*3
#goal_x=[1.5, 2.5, 1.5, -3.5, -3.25, 3, -0.5, 0, -3.25, 2, -3.25, -3, 3, 0, -4.5, -11, -3, -3.25,-2.75, -1, 0.0]
#goal_y=[0, 2.5, 4.5, 2, -2.75, -7, 6.5, 2.5, -0.25, 12, 7, 3, -1, -1.5, -1.75, 2.5, -4, 10, -9, -0.5, 0.0]
scan_data=[]
front = 0.0
left = 0.0
right = 0.0

count = Twist()
# function to get the position of the robot 
def position_robot(msg):
    global x
    global y
    global theta

    x = msg.pose[1].position.x
    y = msg.pose[1].position.y

    quatern = ([msg.pose[1].orientation.x, msg.pose[1].orientation.y, msg.pose[1].orientation.z, msg.pose[1].orientation.w])
    euler = euler_from_quaternion(quatern)
    theta = euler[2]
# function to retrieve the scan data
def get_scan_data(msg1):
    global scan_data,front,left,right
    scan_data=msg1.ranges
    front = min(scan_data[0:10]+scan_data[349:359])
    left = min(scan_data[40:80])
    right = min(scan_data[260:300])
    #return scan_data

# function to get the length of the scan data
def get_length(scan_data):
	return len(scan_data)
# function to get the index of the closest point
def get_index_of_closest_point(scan_data):
        m = min(i for i in scan_data if i > 0)
        index_min_dist = scan_data.index(m)
	return index_min_dist
# function to get the angle of the closest point
def get_angle_of_closest_point(scan_data):
        angle_min_dist = angle_min+get_index_of_closest_point(scan_data)*angle_incr
	return angle_min_dist
# function to get move the turtle bot forward
def move_forward():
        count.linear.x = 0.1
        count.angular.z = 0.0
# function to get the turtle bot turn towards the goal
def turn_goal_direction():
    count.linear.x = 0.0
    count.angular.z = rotation_direction*(0.1 + ((0.2/3.14)*abs(angle_to_goal2 - theta)))

# function to get the turtle bot move left
def turn_left():
        count.linear.x = 0.0
        count.angular.z = 0.1
# function to get the turtle bot move right
def turn_right():
        count.linear.x = 0.0
        count.angular.z = -0.1
# function to get the turtle bot stop
def stop():
    count.linear.x = 0.0
    count.angular.z = 0.0
# function to get the turtle bot move right when obstable faces it 
def move_right_obst():
    for b in range(0,95):
    	turn_right()
        pub.publish(count)
        rate = rospy.Rate(5)
        rate.sleep()
# function to get the turtle bot move left when obstable faces it
def move_left_obst():
    for b in range(0,95):
    	turn_left()
        pub.publish(count)
        rate = rospy.Rate(5)
        rate.sleep()
# function to get the turtle bot move ahead when the bot move right after obstacle detection
def move_ahead():
    for a in range(0,10):
        count.linear.x = 0.1
        count.angular.z = 0.0
        rate = rospy.Rate(5)
        pub.publish(count)
        rate.sleep()
# function to get goal fron /goals
def get_goals(message):
    global goal_points
    goal_points= message.goals
    #return goal_points#print goal_points


rospy.init_node('mini_prj')
sub1=rospy.Subscriber('/goals', PointArray, get_goals)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/scan', LaserScan, get_scan_data)
#rospy.sleep(5)
model_state_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, position_robot)
rospy.sleep(5)
#[0, 2.5, 4.5, 2, -2.75, -7, 6.5, 2.5, -0.25, 12, 7, 3, -1, -1.5, -1.75, 2.5, -4, 10, -9, -0.5, 0.0]
flag=0.0
i=0
rotation_direction=1.0
scan_data1=[0]
scan_data2=[0]
inc_x=[0.0]*20#[0]*len(goal_x)
inc_y=[0.0]*20#[0]*len(goal_y)
r=rospy.Rate(10)
while not rospy.is_shutdown():
          pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
          sub = rospy.Subscriber('/scan', LaserScan, get_scan_data)
          rospy.sleep(2)
          #print goal_points
          inc_x[i]=goal_points[i].x-x
          inc_y[i]=goal_points[i].y-y
          angle_to_goal2=atan2(inc_y[i],inc_x[i]) # logic obtained fron robotigniteacademy.com
          rotation_direction = np.sign(angle_to_goal2 - theta)
          if abs(inc_x[i])>0.1 or abs(inc_y[i])>0.1: # to check if bot is not near the goal
             if abs(angle_to_goal2 - theta) > np.pi : # to check if angle of the bot is not towards the goal 
                rotation_direction = rotation_direction*(-1)
             if abs((angle_to_goal2)-(theta))>0.2:# to check if the angle of the bot is towards goal
                turn_goal_direction()
             if abs((angle_to_goal2)-(theta))<0.2:
                if front>0.5: # to check if there is no obstacle in the front 
                   move_forward()
                if front<0.5: # condition when obstacle found infront of the turtle bot 
                     move_right_obst()
                     move_ahead()
          if abs(inc_x[i])<0.1 and abs(inc_y[i])<0.1: # condition to check if the goal is reached
             if i==19:
                stop()
                pub.publish(count)
                print '---------------------------------------------------'
                print 'goal',i+1,'reached x:',x,'y:',y, 'All goals reached'
                print '---------------------------------------------------'
                break
             stop()
             print '---------------------------------------------------'
             print 'goal',i+1,'reached x:',x,'y:',y
             flag=1.0
             i+=1
             print 'moving towards: ',goal_points[i].x,' ',goal_points[i].y
          pub.publish(count)
