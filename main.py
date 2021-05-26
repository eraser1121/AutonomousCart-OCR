import serial
import cv2
import numpy as np

ser = serial.Serial('/dev/ttyAMA0',115200)
if(ser.isOpen()):
	print("open")

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet('yolov3-tiny_best.weights','yolov3-tiny.cfg')

# YOLO NETWORK 재구성
"""
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
"""
classes = ['box']
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

frame_num = 0

while VideoSignal.isOpened():
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    if ret is False:
        break
    if frame_num != 20:
        frame_num += 1
    elif frame_num == 20:
        frame_num = 0

        h, w, c = frame.shape
       
   
        # YOLO 입력
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
         True, crop=False)
        YOLO_net.setInput(blob)
        outs = YOLO_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:

            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.4:
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

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

       
        if confidences:
            bestscore = confidences.index(max(confidences))
            best_x, best_y, best_w, best_h = boxes[bestscore]
            center_best_x = best_x + best_w/2
            new_frame = frame 
            cv2.rectangle(frame, (best_x, best_y), (best_x + best_w, best_y + best_h), (0, 0, 255), 5)
            
            if best_x > 320 :
                print("오른쪽으로 이동")
                ser.write(serial.to_bytes([int('1',16)]))

            elif best_x + best_w < 320 :
                print("왼쪽으로 이동")
                ser.write(serial.to_bytes([int('2',16)]))

            else :
                print("직진")
                cv2.imwrite('cap_img.jpg', new_frame)

                ser.write(serial.to_bytes([int('3',16)]))
                break;


        """
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                score = confidences[i]
                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, 
                (255, 255, 255), 1)
        """
    

        cv2.imshow("YOLOv3", new_frame)

        if cv2.waitKey(100) > 0:
            break
"""
#key = '1' # stop
#key = '2' # forward
#key = '3'  # backward
#key = '4' #move robot arm
key = str(input())
ser.write(serial.to_bytes([int(key, 16)]))

ser.close()
"""
