import socket
import moter
import time
import threading
import time
switch=-1
def sub_server():
    global switch
    localIP = "192.168.0.43"
    localPort = 8080
    bufferSize = 1024
    msgFromServer = "Hello UDP Client"
    bytesToSend = str.encode(msgFromServer)
    # 데이터그램 소켓을 생성 

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # 주소와 IP로 Bind 
    UDPServerSocket.bind((localIP, localPort))
    # 들어오는 데이터그램 Listen 
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) 
    message = bytesAddressPair[0] 
    address = bytesAddressPair[1] 
    clientMsg = format(message)
    print(clientMsg)
    UDPServerSocket.close()
    switch=switch*(-1)
    

while 1:
    if switch==(-1):
        switch=switch*(-1)
        t1=threading.Thread(target=sub_server)
        t1.start()
    print("ssss")
    time.sleep(0.5)



