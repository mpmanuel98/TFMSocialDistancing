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


"""
Script
----------
"""

print("Starting pre-processing...")

faces, labels, subject_names = OFP.create_recognition_structures("training_images")
recognizer = OFP.Recognizer("eigenfaces", faces, labels, subject_names)

print("Pre-processing finished!")

print("\nTV control process initiated.")

person1_counter = 0
person2_counter = 0
person1_name = subject_names.get(0)
person2_name = subject_names.get(1)
range1_counter = 0
range2_counter = 0
range3_counter = 0
range4_counter = 0
counter_limit = 3
refresh_time = 3600
detected_faces = []

while True:
    img = FWC.take_capture(camera_url)

    pil_image = Image.open(io.BytesIO(img))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    people = recognizer.predict(image)

    if people is None:
        print("No faces detected.")
    else:
        for person in people:
            print(person[0], person[1])
            if(person[1] < 1000.0):
                recognized_name = person[0]
                if(recognized_name == person1_name):
                    person1_counter += 1
                elif(recognized_name == person2_name):
                    person2_counter += 1
            else:
                detected_faces = AFA.detect_face(
                    img, "detection_01", "recognition_02")
                if (detected_faces is None):
                    continue
                else:
                    for face_info in detected_faces:
                        age = face_info.get("age")
                        print(str(age) + " ages person detected.")
                        if(age < 18):
                            range1_counter += 1
                        elif((age >= 18) and (age < 30)):
                            range2_counter += 1
                        elif((age >= 30) and (age < 60)):
                            range3_counter += 1
                        elif(age >= 60):
                            range4_counter += 1

    if((person1_counter == counter_limit) and (person2_counter == counter_limit)):
        print(person1_name, "and", person2_name,
              "recognized, switching source to HDMI 1...")
        STV.set_hdmi_source(1)
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(person1_counter == counter_limit):
        print(person1_name, "recognized, opening Netflix...")
        STV.set_app("netflix")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(person2_counter == counter_limit):
        print(person2_name, "recognized, opening Spotify...")
        STV.set_app("spotify")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range1_counter == counter_limit):
        print("Person of age range 1 detected, opening Clan TV...")
        STV.set_app("clantv")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range2_counter == counter_limit):
        print("Person of age range 2 detected, opening YouTube")
        STV.set_app("youtube")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range3_counter == counter_limit):
        print("Person of age range 3 detected, opening Amazon Prime Video...")
        STV.set_app("prime-video")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range4_counter == counter_limit):
        print("Person of age range 4 detected, opening Meteonews.TV...")
        STV.set_app("meteonews")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(len(detected_faces) >= 3):
        print("Large group of people detected, it's time to party!")
        STV.set_app("party")
        person1_counter, person2_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    else:
        STV.set_power_status(False)
