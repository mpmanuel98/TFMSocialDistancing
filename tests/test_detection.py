import cv2
import modules.ocv_face_processing as OFP
import numpy as np
from PIL import Image

"""
pil_image = Image.open("C:/Users/mpman/Desktop/243543W.jpg")
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
"""
cap = cv2.VideoCapture()
for i in range(0,9):
    cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")
    ret, image = cap.read()

    faces = OFP.detect_faces(image, 5)

    try:
        for face in faces:
            x, y, w, h = face
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    except:
        print("NO FACES DETECTED :(")
    finally:
        name = "test_image_" + str(i) + ".png"
        cv2.imwrite(name, image)
        cap.release()
