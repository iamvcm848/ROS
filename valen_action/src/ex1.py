#! /usr/bin/env python
import rospy
import actionlib
import time
from std_msgs.msg import Empty
from valen_action.msg import VcmdroneAction,VcmdroneFeedback,VcmdroneResult

class VcmClass(object):
    fb_obj=VcmdroneFeedback()
    rs_obj=VcmdroneResult()

    def __init__(self):
        self.asv=actionlib.SimpleActionServer("vcm_as",VcmdroneAction,self.a_feedback,False)
        self.asv.start()
        self.takeoff=rospy.Publisher('/drone/takeoff',Empty, queue_size=1)
        self.land=rospy.Publisher('/drone/land',Empty, queue_size=1)
        self.t_obj=Empty()
        self.l_obj=Empty()
    
    def a_feedback(self,goal):
        success=True
        rate=rospy.Rate(1)
        print(goal.move)
        self.fb_obj.status=goal.move
    
        if self.asv.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled !!!')
            self.asv.set_preempted()
            success=False
        
        if goal.move=='TAKEOFF':
            self.asv.publish_feedback(self.fb_obj)
            i=0
            while i<=3:
                self.takeoff.publish(self.t_obj)
                time.sleep(1)
                i+=1

        if goal.move=='LAND':
            self.asv.publish_feedback(self.fb_obj)
            i=0
            while i<=3:
                self.land.publish(self.l_obj)
                time.sleep(1)
                i+=1
                
        rate.sleep()

        if success:
            print('Action done !!!')
            self.asv.set_succeeded(self.rs_obj)
      
if __name__ == '__main__':
    rospy.init_node('vcm_fly')
    VcmClass()
    rospy.spin()