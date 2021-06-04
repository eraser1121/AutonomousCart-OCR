import serial
import cv2
import numpy as np
import ocr_image
import findDB

ser = serial.Serial('/dev/ttyAMA0',115200)
if(ser.isOpen()):
	print("Serial Communication in operation")

LiveCam = cv2.VideoCapture(0)
YOLO_net = cv2.dnn.readNet('yolov3-tiny_best.weights','yolov3-tiny.cfg')

classes = ['box']
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

frame_num = 0
count = 0
while LiveCam.isOpened():
    
    ret, frame = LiveCam.read()
    if ret is False:
        print("No Video Input")
        break
    if frame_num != 20:
        frame_num += 1
    elif frame_num == 20:
        frame_num = 0

        h, w, c = frame.shape
       
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    dw = int(detection[2] * w)
                    dh = int(detection[3] * h)
                    x = int(center_x - dw / 2)
                    y = int(center_y - dh / 2)
                    boxes.append([x, y, dw, dh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

       
        if confidences :
            bestscore = confidences.index(max(confidences))
            best_x, best_y, best_w, best_h = boxes[bestscore]
            
            if best_x > 310 :
                print("오른쪽으로 이동")
                ser.write(serial.to_bytes([int('1',16)]))

            elif best_x + best_w < 330 :
                print("왼쪽으로 이동")
                ser.write(serial.to_bytes([int('2',16)]))

            else :
                print("직진")
                count = 1


            cv2.rectangle(frame, (best_x, best_y), (best_x + best_w, best_y + best_h), (0, 0, 255), 5)
            cv2.putText(frame, 'box', (best_x, best_y - 20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)

        cv2.imshow("YOLOv3", frame)
        if count == 1 :
            if cv2.waitKey(100) > 0 :
                cv2.imwrite('cap_img.jpg', frame)
                ser.write(serial.to_bytes([int('3',16)]))
                break
            

        if cv2.waitKey(100) > 0:
            break


image = cv2.imread("cap_img.jpg")
template = cv2.imread("myform.jpg")

ocr_result = ocr_image.ocr(image, template)

(name, result) = ocr_result["name"]
(address, result) = ocr_result["address"]
(detail_address, result) = ocr_result["detail_address"]

name = name.replace(" ","")
address = address.replace(" ","")
detail_address = detail_address.replace(" ","")

print(name)
print(address)
print(detail_address)

name = findDB.find_name(name)
detail_address = findDB.find_address(detail_address)

destination_num = findDB.set_destination(name, detail_address)
print (destination_num)