import socket
import time



def server(class_):
    serverAddressPort = ("192.168.0.43", 8080)
    bufferSize = 1024 # 클라이언트 쪽에서 UDP 소켓 생성

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # 생성된 UDP 소켓을 사용하여 서버로 전송 
    if class_ ==2:
        msgFromClient = "G"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
    if class_ ==3:
        msgFromClient = "R"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
    if  class_ ==5:
        msgFromClient = "3"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
    if  class_ ==6:
        msgFromClient = "6"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
    if  class_ ==4:
        msgFromClient = "S"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
    if  class_ ==7:
        msgFromClient = "T"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()    
    elif class_ ==50 or class_ ==0 or class_ ==1 or class_ ==8 or class_ ==9:
        msgFromClient = "N"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()    
    return 