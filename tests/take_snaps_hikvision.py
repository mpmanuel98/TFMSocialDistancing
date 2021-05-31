import time
import cv2

cap = cv2.VideoCapture()
for i in range(1, 100):
    cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")
    _, frame = cap.read()

    name = "image_hikvision_" + str(i)
    name = name + ".png"
    cv2.imwrite(name,frame)

    cap.release()
    time.sleep(2)
