#! /usr/bin/env python

import rospy
import time
import actionlib
from valen_action.msg import VcmdroneAction,VcmdroneFeedback,VcmdroneResult,VcmdroneGoal

# We create some constants with the corresponing vaules from the SimpleGoalState class
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4


def feedback_callback(feedback):
    print("current state :",feedback.status)
    
# initializes the action client node
rospy.init_node('vcm_fly_client')

action_server_name = '/vcm_as'
client = actionlib.SimpleActionClient(action_server_name, VcmdroneAction)

# waits until the action server is up and running
rospy.loginfo('Waiting for action Server '+action_server_name)
client.wait_for_server()
rospy.loginfo('Action Server Found...'+action_server_name)

# creates a goal to send to the action server
goal = VcmdroneGoal()
client.send_goal(goal, feedback_cb=feedback_callback)
state_result = client.get_state()
rate = rospy.Rate(1)
rospy.loginfo("state_result: "+str(state_result))

while state_result < DONE:
    i=0
    while i<10:
        if i<5:
            goal.move='TAKEOFF'
        if i>=5:
            goal.move='LAND'
        client.send_goal(goal, feedback_cb=feedback_callback)
        rate.sleep()
        i+=1


    
    
    