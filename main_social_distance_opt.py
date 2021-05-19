"""
Script main_social_distance_opt.py.

Description

Also a function is defined:
    function(variable)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import argparse
import io
import time
from datetime import datetime

import cv2
import mysql.connector
import numpy as np
from PIL import Image
from scipy.spatial import distance as dist

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

"""
Parameters
----------
"""
# define the camera to use (hikvision | foscam)
CAMERA = "hikvision"

if(CAMERA == "foscam"):
    # define the minimum safe distance (in cms) that two people can be from each other
    MIN_DISTANCE = 150

    # define the relation between pixels and cms (pixels, cms)
    RELATION = (16, 3)

    # define the minimum size in pixels that a face size must be
    MIN_SIZE = 50

    # define the focal length of the camera (F = (P x D) / W)
    FOCAL_LENGTH = 2.8
elif(CAMERA == "hikvision"):
    # define the minimum safe distance (in cms) that two people can be from each other
    MIN_DISTANCE = 150

    # define the relation between pixels and cms (pixels, cms)
    RELATION = (36, 3)

    # define the minimum size in pixels that a face size must be
    MIN_SIZE = 100

    # define the focal length of the camera (F = (P x D) / W)
    FOCAL_LENGTH = 2305
else:
    exit()

# define the conector to the mysql database
db_connector = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="tfm_control_aula"
)

db_cursor = db_connector.cursor(buffered=True)

# define the total number of images to take
NUM_IMAGES = 20

# define the refresh time (in seconds) between images taken
FREQUENCE = 40 / (NUM_IMAGES)

# define the code of the sesion
parser = argparse.ArgumentParser(description="Subject.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--subject_code", help="The code of the subject.", type=str, default="71142104")
args = parser.parse_args()

CODE = int(args.subject_code)

# define the actual date
ACTUAL_DATE = (datetime.now()).strftime('%Y-%m-%d')

"""
Script
----------
"""
print("Starting pre-processing...")

faces, labels, subject_names = OFP.create_recognition_structures("training_images")
recognizer = OFP.Recognizer("fisherfaces", faces, labels, subject_names)

print("Pre-processing finished!")

for iteration in range(1, 10):

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

    faces = OFP.detect_faces(image, MIN_SIZE)

    if faces is None:
        continue

    centroids = []
    distances = []
    centroids_ids = dict()
    for face in faces:
        x, y, w, h = face
        
        face_cropped = image[y:y+h, x:x+w]
        person = recognizer.identify_single_face(face_cropped)
        print(person)
        # compute and store the centroids and distances to camera of the faces detected
        centroid = (int((x+(x+w))/2), int((y+(y+h))/2))
        # Distance = FocalLength in mm * (Real object width in mm) / (Virtual object width in px)
        distance = (15 * FOCAL_LENGTH) / ((x+w) - x)

        print(distance)
        distances.append(distance)
        centroids.append(centroid)

        # save the correspondence between the centroid and the person
        if(person[1] < 2000):
            centroids_ids[person[0]] = centroid

        # plot the centroid and the rectangle arround the faces
        cv2.circle(image, centroid, radius=0, color=(0, 255, 0), thickness=3)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # compute the euclidean distance between the centroids
    dist_comp = dist.cdist(centroids, centroids, metric="euclidean")
    print(dist_comp)

    violations = dict()
    i = 0
    j = 0
    for i in range(0, dist_comp.shape[0]):
        relations = []
        for j in range(0, dist_comp.shape[1]):
            if(dist_comp[i, j] == 0):
                continue

            dist_diff = abs(distances[i] - distances[j])
            dist_ij = dist_comp[i, j] * RELATION[1] / RELATION[0]
            dist_final = np.sqrt(pow(dist_diff, 2) + pow(dist_ij, 2))

            print("Distancia final es " + str(dist_final))

            # check if the distance between two centroid pairs is less than the threshold
            if (dist_final < MIN_DISTANCE) and (dist_final > 0):
                relations.append((centroids[j], dist_final))
            j+=1

        if len(relations) == 0:
            continue

        violations[centroids[i]] = relations
        i+=1

    num_violations = 0
    for key, value in violations.items():
        for rel_tuple in value:

            cv2.line(image, key, rel_tuple[0], (0, 0, 255), thickness=1, lineType=8)

            midPoint = (int((key[0] + rel_tuple[0][0]) / 2), int((key[1] + rel_tuple[0][1]) / 2))

            cv2.putText(image, str(round(rel_tuple[1], 2)) + "cm", midPoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # insert alert in the db           
            try:  
                for sub_key, sub_value in centroids_ids.items():
                    if(sub_value == key):
                        person_id1 = sub_key
                    if(sub_value == rel_tuple[0]):
                        person_id2 = sub_key

                sql = "INSERT INTO alertas_distancia (fecha, codigo, dni_estudiante1, dni_estudiante2) VALUES (%s, %s, %s, %s)"
                sql_values = (ACTUAL_DATE, CODE, person_id1, person_id2)
                db_cursor.execute(sql, sql_values)
                db_connector.commit()

                if(db_cursor.rowcount == 1):
                    print("1 alert inserted in the DB.")
            except:
                print("Alert already inserted in the DB with the provided IDs.")

            num_violations += 1

    text = "Violaciones de la Distancia de Seguridad: " + str(num_violations / 2)
    cv2.putText(image, text, (10, image.shape[0] - 25), cv2.FONT_HERSHEY_COMPLEX, 0.55, (255, 255, 255), 2)

    name = "iteracion_" + str(iteration) + ".png"
    cv2.imwrite(name, image)

    # wait some time (frequence)
    time.sleep(FREQUENCE)
