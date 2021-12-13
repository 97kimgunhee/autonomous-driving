from cv2 import QT_STYLE_OBLIQUE
from geometry_msgs.msg import Twist
import math 
import rospy
import numpy as np
import time
speed=Twist()
speed.linear.x=0.1
rospy.init_node("test_cmd_vel")
rate=rospy.Rate(500)
pub=rospy.Publisher("/cmd_vel",Twist,queue_size=1)
x=0.0
z=0.0

#-----차선인식-------------------------------------------------------
def moter(L,R,midx,midy):
    global x,z
    
    #오차각도 구하기--------------------
    a=(173-midx)
    b=(240-midy)
    angle=math.atan2(a,b)
    angle=round(math.degrees(angle))
    #----차선 둘다 인식----------
    if R!=0 and L!=0 : 
        #---------------------------------
        if -10<angle<10: #직진으로 인식   
            x=0.3   # o all x=0.1
            z=0.0
        if -10>angle<-30: #차선을 약간 벗어나거나, 차선을 물고있을때 차선 중앙 찾아가기
            x=0.3
            z=-0.4
        if 10<angle<30: #차선을 약간 벗어나거나, 차선을 물고있을때 차선 중앙 찾아가기
            x=0.3
            z=0.4
        if angle>=35: #코너 돌기
            x=0.3
            z=1.2
        if angle<=-35: #코너 돌기
            x=0.3
            z=-1.2

    #------오른쪽 차선 인식실패----    print(degree_L)
    if R==0 and L!=0:
        x=0.2          # o x= 0.1                   2
        z=-0.1        # z=0.3                    1                        
        #print("오른쪽 차선 인식실패")

    #----------------------------
    #------왼쪽 차선 인식실패-----
    if R!=0 and L==0:
        x=0.2
        z=0.1
        #print("왼쪽 차선 인식실패")
        #----차선 검출 실패----------
    if R==0 and L==0:
        x=0.0
        z=0.0
        
        
    speed.linear.x=x
    speed.angular.z=z
  
