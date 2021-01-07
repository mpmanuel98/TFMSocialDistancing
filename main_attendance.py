"""
Script main_attendance.py.

Description

Also a function is defined:
    function(variable)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import argparse
import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

"""
Parameters
----------
"""

# define the camera to use
# 1.- hikvision
# 2.- foscam
CAMERA = "hikvision"

"""
Script
----------
"""

print("Starting pre-processing...")

faces, labels, subject_names = OFP.create_recognition_structures("training_images")
print(len(faces))
print(len(labels))
recognizer = OFP.Recognizer("fisherfaces", faces, labels, subject_names)

print("Pre-processing finished!")

#str(time.strftime("%d_%m_%Y-%H.%M.%S"))
filename = "Asistencia el " + str(time.strftime("%d_%m_%Y")) + ".txt"
attendance_reg = open(filename, "w")
people_control = []

for iteration in range(1,20):

    if(CAMERA == "foscam"):
        img = FWC.take_capture("http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?")
        pil_image = Image.open(io.BytesIO(img))
        image = np.array(pil_image)
    elif(CAMERA == "hikvision"):
        cap = cv2.VideoCapture()
        cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")
        ret, image = cap.read()
    else:
        exit()

    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    people = recognizer.predict(image_gray)

    if people is None:
        print("No people detected.")
    else:
        for person in people:
            if(person[0] in people_control):
                print("Person already recognized.")
                continue
            else:
                people_control.append(person[0])

            if(person[1] < 2000.0):
                print(person[0], "recognized.")
                line_reg = person[0] + "\n"
                attendance_reg.write(line_reg)

    # wait 10 minutes (600)
    time.sleep(1)
