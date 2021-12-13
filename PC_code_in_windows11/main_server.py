
import socket
import numpy
import cv2
import numpy as np
import threading
print(cv2.__version__)
YOLO_net = cv2.dnn.readNet("yolov3-tiny_20000.weights","yolov3-tiny.cfg")

def work1(find_class2): 
    import sub_client
    sub_client.server(find_class2)
    
def video(frame):
    # YOLO NETWORK 재구성
    who_are_you=50
    classes = []
    with open("obj .names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = YOLO_net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 1))

        # 웹캠 프레임
    h, w, c = frame.shape

        # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (312, 312), (0, 0, 0),#416 
    True, crop=False)#이미지를 전처리하고 마지막으로 로드 된 사전 학습 된 모델로 이 blob을 전달
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)
    #outs = 감지결과
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                    # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)

                    # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                    
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                who_are_you=class_id
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
    colors = np.random

    font = cv2.FONT_HERSHEY_PLAIN
    colors = (255,0,0)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            #color = colors[i]

                # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 1)
            cv2.putText(frame, label + " " + confidence, (x, y + 20), font, 2, (255,0,0), 1)
    cv2.imshow("test",frame)
    return who_are_you
cv2.destroyAllWindows()

UDP_IP ='192.168.0.15'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (320, 240))
while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]

    if data[0] == 19:
        for i in range(20):
            picture += s[i]
 
        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(240, 320, 3)
        who_are_you1=video(frame)
        t1=threading.Thread(target=work1,args=(who_are_you1,))
        t1.start()
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break