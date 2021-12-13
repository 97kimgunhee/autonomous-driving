import socket
import cv2
import threading
import numpy as np
import find_midxy
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
switch=-1
x=0.1
z=0.0
L=0
R=0
midx=0 
midy=0
#-----차선인식-------------------------------------------------------
def moter(L,R,midx,midy,km):
    global x,z,speed
    #오차각도 구하기--------------------
    a=(173-midx)
    b=(240-midy)
    angle=math.atan2(a,b)
    angle=round(math.degrees(angle))
    #----차선 둘다 인식----------
    if R!=0 and L!=0 : 
        #---------------------------------
        if -15<=angle<=15: #직진으로 인식   
            x=km   # o all x=0.1
            z=0.0
        if -15>angle<-30: #차선을 약간 벗어나거나, 차선을 물고있을때 차선 중앙 찾아가기
            x=km
            z=-0.3
        if 15<angle<30: #차선을 약간 벗어나거나, 차선을 물고있을때 차선 중앙 찾아가기
            x=km
            z=0.3
        if angle>=30: #코너 돌기
            x=km
            z=1.0
        if angle<=-30: #코너 돌기
            x=km
            z=-1.0 

    #------오른쪽 차선 인식실패----    print(degree_L)
    if R==0 and L!=0:
        x=0.2      # o x= 0.1                   2
        z=-0.2     # z=0.3                    1                        
        #print("오른쪽 차선 인식실패")

    #----------------------------
    #------왼쪽 차선 인식실패-----
    if R!=0 and L==0:
        x=0.2
        z=0.2
        #print("왼쪽 차선 인식실패")
        #----차선 검출 실패----------
    if R==0 and L==0:
        x=0.1
        z=0.0
        
        
    speed.linear.x=x
    speed.angular.z=z  
    pub.publish(speed)
#-------------------------------------------------------------------
def DetectLineSlope(src):
    global L,R,midx,midy
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    can = cv2.Canny(gray, 150, 200, None, 3)
    height = can.shape[0]
    rectangle = np.array([[(50, height-20), (70, 170), (244, 170), (264, height-20)]]) #ROI 범위지정정
    mask = np.zeros_like(can)
    
    cv2.fillPoly(mask, rectangle, 255)
    masked_image = cv2.bitwise_and(can, mask)
    ccan = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)

    line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20 , minLineLength=25, maxLineGap=13) #검출 민감도 
    line_R = np.empty((0, 5), int)  
    line_L = np.empty((0, 5), int)  
    if line_arr is not None:
        line_arr2 = np.empty((len(line_arr), 5), int)
        for i in range(0, len(line_arr)):
            temp = 0
            l = line_arr[i][0]
            line_arr2[i] = np.append(line_arr[i], np.array((np.arctan2(l[1] - l[3], l[0] - l[2]) * 180) / np.pi))
            if line_arr2[i][1] > line_arr2[i][3]:
                temp = line_arr2[i][0], line_arr2[i][1]
                line_arr2[i][0], line_arr2[i][1] = line_arr2[i][2], line_arr2[i][3]
                line_arr2[i][2], line_arr2[i][3] = temp
            if line_arr2[i][0] < 170 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 20): #중간지점,각도,
                line_L = np.append(line_L, line_arr2[i])
            elif line_arr2[i][0] > 180 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 20):
                line_R = np.append(line_R, line_arr2[i])
    line_L = line_L.reshape(int(len(line_L) / 5), 5)
    line_R = line_R.reshape(int(len(line_R) / 5), 5)



    try:
        line_L = line_L[line_L[:, 0].argsort()[-1]]
        degree_L = line_L[4]
        cv2.line(ccan, (line_L[0], line_L[1]), (line_L[2], line_L[3]), (153, 153,166), 10, cv2.LINE_AA) #왼쪽 차선 굵기 및 색상
    except:
        degree_L = 0

    try:        
        line_R = line_R[line_R[:, 0].argsort()[0]]
        degree_R = line_R[4]
        cv2.line(ccan, (line_R[0], line_R[1]), (line_R[2], line_R[3]), (153, 153, 166), 5, cv2.LINE_AA) #오른쪽 차선 굵기 및 색상
    except:
        degree_R = 0
 
    if degree_R!=0 and degree_L!=0: 
        midx,midy = find_midxy.midxy(line_L[0],line_L[1],line_R[0],line_R[1]) #방향성x,y
    mimg = cv2.addWeighted(src, 1, ccan, 1, 0)
    L=degree_L
    R=degree_R

    return mimg
   #------------------------------------------ 

def sub_server():
    global speed
    global switch
    global L,R,midx,midy
    T_km=0
    
    localIP = "192.168.0.43"
    localPort = 8080
    bufferSize = 1024
    # 데이터그램 소켓을 생성 
    
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # 주소와 IP로 Bind 
    
    UDPServerSocket.bind((localIP, localPort))
    # 들어오는 데이터그램 Listen 
    while 1:
        except_=0
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) 
        message = bytesAddressPair[0] 
        clientMsg = format(message)

        #-Green OR 60KM---------------------------
        if clientMsg=="b'G'":
            speed.linear.x=0.25
            speed.angular.z=0.0
            except_=1
            pub.publish(speed)
        #-----------------------------------------
        #-60KM------------------------------------
        if clientMsg=="b'6'":
            speed.linear.x=0.35
            speed.angular.z=0.0
            except_=1
            pub.publish(speed)
        #-----------------------------------------
        #-Red OR STOP-----------------------------  
        if  clientMsg=="b'S'":
            speed.linear.x=0.0
            speed.angular.z=0.0
            except_=1
            pub.publish(speed)
        #-----------------------------------------
        #-Red-----------------------------  
        if clientMsg=="b'R'" :
            speed.linear.x=0.0
            speed.angular.z=0.0
            except_=1
            pub.publish(speed)
            time.sleep(0.125)
        #-----------------------------------------
        #-30KM------------------------------------
        if clientMsg=="b'3'":
            speed.linear.x=0.1
            speed.angular.z=0.0
            except_=1
            pub.publish(speed)
        #-----------------------------------------
        #-T-----------------------------------
        if clientMsg=="b'T'":
            speed.linear.x=0.0
            speed.angular.z=-1.8
            except_=1
            T_km=1
            pub.publish(speed)
            #time.sleep(0.1)
        #-----------------------------------------
        #-no_find---------------------------------
        elif clientMsg=="b'N'" and except_==0:

            except_=0
            if T_km==1:
                moter(L,R,midx,midy,0.15)
            else:
                moter(L,R,midx,midy,0.25)
            
        
        #-----------------------------------------     
UDP_IP = '192.168.0.15'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture("/dev/video0",cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320); # 가로
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240); # 세로
t1=threading.Thread(target=sub_server)
t1.start()
  

while True:
    ret, frame = cap.read()
    frame_=DetectLineSlope(frame)
    #-------------------------------------------------------
 
    
    #-------------------------------------------------------
    d = frame_.flatten()
    s = d.tostring()
    for i in range(20):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #-------------------------------------------------------