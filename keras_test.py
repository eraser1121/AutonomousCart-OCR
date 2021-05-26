from IPython.display import display
from PIL import Image
from yolo import YOLO
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import tensorflow.compat.v1.keras.backend as K
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

def objectDetection(file, model_path, class_path):
    yolo = YOLO(model_path=model_path, classes_path=class_path, anchors_path='model_data/tiny_yolo_anchors.txt')
    image = Image.open(file)
    result_image = yolo.detect_image(image)
    result_image.save('test.jpg','JPEG')

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()
    
yolo = YOLO(model_path='model_data/yolo_tiny_best.h5', classes_path='data/box/classes.txt', anchors_path='model_data/tiny_yolo_anchors.txt')

# loop through frames
while webcam.isOpened():
    status, frame = webcam.read()

    if not status:
        break
    '''
    cv2.imwrite('frame.jpg', frame)
    objectDetection('frame.jpg', 'model_data/yolo_tiny_best.h5', 'data/box/classes.txt')
    out = cv2.imread('test.jpg')
    '''
    cv2.imwrite('frame.jpg', frame)
    tst = Image.open('frame.jpg')
    out = yolo.detect_image(tst)
    out.save('test.jpg', 'JPEG')
    out = cv2.imread('test.jpg')
    cv2.imshow("Real-time object detection", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()


