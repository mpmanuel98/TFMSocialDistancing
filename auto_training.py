"""
Script auto_capture.py.

"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import argparse
import io
import os
import time
import cv2
import shutil

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

if not os.path.exists("training_images/cropped_temp_faces"):
    os.makedirs("training_images/cropped_temp_faces")

"""
print("Starting the general face detection process...")

face_id = 0
for iteration in range(1,5):

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

    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(imageRGB)

    faces = OFP.detect_faces(image, 150)

    if faces is None:
        continue

    for face in faces:
        x, y, w, h = face
        pil_img = pil_img.crop((x, y, x+w, y+h))
        pil_img.save("training_images/cropped_temp_faces/image_" + str(face_id) + ".png")
        face_id += 1
    
    print("Captures taken and saved!")
    time.sleep(1)

print("General face detection process finished.")
"""

print("Starting the classification process...")

for image_name in os.listdir("training_images/cropped_temp_faces"):

    image = cv2.imread("training_images/cropped_temp_faces/" + image_name)

    cv2.imshow("Press any key to start the classification...", image)
    cv2.waitKey(0)

    print("\nOptions list:\n")
    people_indexes = dict()
    index = 1
    for people_dirs in os.listdir("training_images"):

        if(people_dirs == "cropped_temp_faces"):
            continue

        print(str(index) + " -> " + people_dirs)
        people_indexes[index] = people_dirs

        index += 1

    people_indexes[index] = "new"
    print(str(index) + " -> Add new person")
    index += 1
    people_indexes[index] = "none"
    print(str(index) + " -> Remove image")

    value_selected = input("\nWho is this person? (select an option from above): ")

    if(int(value_selected) == int(len(people_indexes) - 1)):

        new_name = input("\nInsert the name of the new person: ")

        if not os.path.exists("training_images/" + new_name):
            os.makedirs("training_images/" + new_name)

        shutil.move("training_images/cropped_temp_faces/" + image_name, "training_images/" + new_name + "/" + image_name)
    elif(int(value_selected) == int(len(people_indexes))):
        os.remove("training_images/cropped_temp_faces/" + image_name)
    else:
        shutil.move("training_images/cropped_temp_faces/" + image_name, "training_images/" + people_indexes.get(int(value_selected)) + "/" + image_name)