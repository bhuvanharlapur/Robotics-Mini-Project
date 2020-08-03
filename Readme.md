# Turtle Bot Programming for Obstacle Avoidance

The below given is a description of the project in which a turtle bot has to reach the goal published in `/goals` topic by launching the goal_publisher launch file.
This may sound a not much a big deal but the turtle bot has to avoid any obstacle facing infront of it and reach the goals. Brief structure of the Mini Project

[[_TOC_]]

## Introduction

To get started we have to launch empty world from turtlebot_gazebo package. To load the predesigned test arena we have to run the following code.

`rosrun gazebo_ros spawn_model -file ~/catkin_ws/src/bh-192135_tier3_miniprj/mini_project_master/model.sdf -sdf -x 2 -y 1 -model mini_project.` 

Gazebo simulation should now look like the screenshot below.

<img src="images/Gazebo_model.png">

Now we are ready for the task.


## Brief Description

The main aim of the project is to create a package that, when launched, will navigate the turtlebot to as many different goal positions as possible that are published on a topic called /goals.

Sr.No| List of Topics       | Subscribed/Published      | Message type    | Message imported from package    | 
:---: | :---         	    | :---                      | :---            | :--- 	                         | 
1    | /goals       	    | Subscribed                | PointArray      | goal-publisher                   |
2    | /gazebo/model_states | Subscribed                | ModelStates     | gazebo-msgs                      |
3    | /scan                | Subscribed                | LaserScan       | sensor-msgs
4    | /cmd_vel             | Published                 | Twist           | geometry-msgs                    |

1. `/goals` topic is subscribed to get the goal points which is published when we launch goal_publisher package.

2. `/gazebo/model_states` topic is subscribed to obtain the position and orintation of the turtlebot in the given environment. The message of this topic contains the details of position and orintation of the 'ground-plane', 'turtlebot3-burger' and 'mini-project'. But we are intrested in the details of turtlebot alone.

3. `/scan` topic is subscribed to get the details of the objects surrounding turtlebot.

4. Depending on the situation appropriate speed is provided to the turtlebot using the topic `/cmd_vel`.


## Algorithm

After launching goal-publisher and the gazebo simulation.

- Subscribe to the /goals, /gazebo/model_states and /scan topic so that we get the goals, position & orientation of the turtlebot and laser scan data respectively.
- While the rospy is not shut down
  - If there the distance between the turtlebot and the goal is grater than 0.1
    -If the angle towards the goal is greater than 20 degrees the bot moves towards the goal
    -If the angle towards the goal is less than 20 degress it stops.
     -If the there is no obstacle in the front the robot moves towards the goal.
     -If there is an obstacle in the front the robot moves towards right and then moves front for a certain distance. and rechecks if there is an obstacle the robot then realligns towards goal 
      and starts moving forward
  - If the distance between the goal and the bot is less than 0.1 then robot stops and starts mving towards the next goal with the same logic as above.


## Implementation

**Logic_Used** 

- To avoid the obstacles and reach the goal as per the logic mentioned in below table.
  The value is `1` if the obstacle is detected and its `0` if it is not detected. 

  |Left|Front|Right|Action|
  |:-:|:--:|:--:|:--|
  |0|0|0|Point towards goal and move forward|
  |0|0|1|Move Forward|
  |0|1|0|Turn right to the temporary goal|
  |0|1|1|Turn left to the temporary goal|
  |1|0|0|Move Forward|
  |1|0|1|Move Forward|
  |1|1|0|Turn right to the temporary goal|
  |1|1|1|Rotate 180 degree|


Because of the advantages of the callback functions i have made callback function for each operations so that it is simpler to code and easy to understand. 

**Call_back functions** 
- To get the all the goals
- To get the scan data and assign the laser ranges for obstacle detection.
- To get the position of the turtlebot which can be used as and when it is needed.

**User defined functions**
- To Move forward left and right and also to move right.

- To move right when the obstacle is in the front.
```python
for b in range(0,95):
    	turn_right()
        pub.publish(count)
        rate = rospy.Rate(5)
        rate.sleep()
```
- To move ahead after turning right.
```python
for a in range(0,10):
        count.linear.x = 0.1
        count.angular.z = 0.0
        rate = rospy.Rate(5)
        pub.publish(count)
        rate.sleep()
```

## Problems Encountered and Solution

**Problem:**

Rotation of Robot towards goal

This something which was particularly challenging as everytime the robot missed the angle towrads the robot would move either colock wise or anti clock wise completely to re allign towards goal and this would be very time consuming and and very tedious

**Solution:**

Angle to goal - determines which quadrant the goal is with respect to turtlebot.
Angle - Angle where the turtlebot is facing.

If the goal is on the left side( less than 180 degrees) then the 'Angle to goal- Angle' would be positive and the bot would move left but if the anle goal would be greater than 180 degress with respect to robot angle then 'Angle to goal- Angle' would be negetive and hence the angulaer speed would multiplied by the by this sign 

Angular Speed= Speed * sign of ('Angle to goal- Angle')
