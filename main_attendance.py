"""
Script main_attendance.py
-------------------------
"""
__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import time
from datetime import datetime

import cv2
import mysql.connector
import numpy as np
from PIL import Image

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

"""
Parameters
----------
"""
SUBJECT = "Cloud Computing"
CODE = 71142104

# define the conector to the mysql database
db_connector = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="asignaturatest"
)

db_cursor = db_connector.cursor(buffered=True)

# define the camera to use (hikvision | foscam)
CAMERA = "hikvision"

# define the total number of images to take
NUM_IMAGES = 5

# define the refresh time (in seconds) between images taken
FREQUENCE = 10 / (NUM_IMAGES)

# define the actual date
ACTUAL_DATE = (datetime.now()).strftime('%Y-%m-%d')

"""
Script
----------
"""
# check if the subject is in the db, if not, insert it
sql = "SELECT * FROM asignatura WHERE codigo = %s"
values = (CODE, )
db_cursor.execute(sql, values)

if(db_cursor.rowcount == 0):
    sql = "INSERT INTO asignatura (codigo, nombre) VALUES (%s, %s)"
    values = (CODE, SUBJECT)
    db_cursor.execute(sql, values)
    db_connector.commit()
    print(db_cursor.rowcount, "subject inserted in the db.")

# check if the session is in the db, if not, insert it
sql = "SELECT * FROM sesion WHERE codigo = %s AND fecha = %s"
values = (CODE, ACTUAL_DATE)
db_cursor.execute(sql, values)

if(db_cursor.rowcount == 0):
    sql = "INSERT INTO sesion (codigo, fecha) VALUES (%s, %s)"
    values = (CODE, ACTUAL_DATE)
    db_cursor.execute(sql, values)
    db_connector.commit()
    print(db_cursor.rowcount, "session inserted in the db.")

print("Starting pre-processing...")

faces, labels, subject_names = OFP.create_recognition_structures("training_images")
recognizer = OFP.Recognizer("fisherfaces", faces, labels, subject_names)

print("Pre-processing finished!")

for iteration in range(1, NUM_IMAGES):
    # take a capture from the IP camera
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
    print(people)

    if people is None:
        print("No people detected.")
    else:
        for person in people:
            if(person[1] < 2000.0):
                print(person[0], "recognized.")

                # insert the person in the db
                try:  
                    sql = "INSERT INTO asistencia (dni, codigo, fecha) VALUES (%s, %s, %s)"
                    values = (person[0], CODE, ACTUAL_DATE)
                    
                    db_cursor.execute(sql, values)
                    db_connector.commit()

                    if(db_cursor.rowcount == 1):
                        print("1 person listed in the DB.")
                except:
                    print("Person already listed in the DB.")

    # wait some time (frequence)
    time.sleep(FREQUENCE)
