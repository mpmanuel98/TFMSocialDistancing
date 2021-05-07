__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import time
import cv2

cap = cv2.VideoCapture()
for i in range(1, 100):
    cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")

    name = "image_hikvision_" + str(i)
    name = name + ".png"

    _, frame = cap.read()
    cv2.imwrite(name,frame)

    cap.release()
    time.sleep(2)
