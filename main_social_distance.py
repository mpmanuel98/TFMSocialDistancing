"""
Script main_social_distance.py.

Description

Also a function is defined:
    function(variable)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import datetime
import time
import io
import os

from scipy.spatial import distance as dist
import cv2
import numpy as np
from PIL import Image

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

if(CAMERA == "foscam"):
    # define the minimum safe distance (in pixels) that two people can be from each other
    MIN_DISTANCE = 1500

    # define the relation between pixels and cms (pixels, cms)
    RELATION = (16, 3)

    # define the minimum size in pixels that a face size must be
    min_size = 50
elif(CAMERA == "hikvision"):
    # define the minimum safe distance (in pixels) that two people can be from each other
    MIN_DISTANCE = 1500

    # define the relation between pixels and cms (pixels, cms)
    RELATION = (36, 3)

    # define the minimum size in pixels that a face size must be
    min_size = 200
else:
    exit()

"""
Script
----------
"""

# str(time.strftime("%d_%m_%Y-%H.%M.%S"))
filename = "Registro del " + str(time.strftime("%d_%m_%Y")) + ".txt"
violations_reg = open(filename, "w")

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

    faces = OFP.detect_faces(image, min_size)

    if faces is None:
        continue

    centroids = []
    #face_index = 0
    for face in faces:
        x, y, w, h = face

        # compute and store the centroids of the faces detected
        centroid = (int((x+(x+w))/2), int((y+(y+h))/2))
        centroids.append(centroid)

        # plot the centroid and the rectangle arround the faces
        cv2.circle(image, centroid, radius=0, color=(0, 255, 0), thickness=3)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

        #face_index += 1

    # compute the euclidean distance between the centroids
    dist_comp = dist.cdist(centroids, centroids, metric="euclidean")

    violations = dict()
    for i in range(0, dist_comp.shape[0]):
        relations = []
        for j in range(0, dist_comp.shape[1]):

            # check if the distance between two centroid pairs is less than the threshold
            if (dist_comp[i, j] < MIN_DISTANCE) and (dist_comp[i, j] > 0):
                relations.append((centroids[j], dist_comp[i, j]))

        if len(relations) == 0:
            continue

        violations[centroids[i]] = relations

    num_violations = 0
    for key, value in violations.items():
        for rel_tuple in value:

            cv2.line(image, key, rel_tuple[0],
                     (0, 0, 255), thickness=1, lineType=8)

            midPoint = (int((key[0] + rel_tuple[0][0]) / 2),
                        int((key[1] + rel_tuple[0][1]) / 2))

            real_distance = rel_tuple[1] * RELATION[1] / RELATION[0]

            cv2.putText(image, str(round(real_distance, 2)) + "cm", midPoint,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            line_reg = str(key) + " con " + str(rel_tuple[0]) + " a las " + str(time.strftime("%H.%M.%S")) + " a una distancia aproximada de: " + str(round(real_distance, 2)) + " cms\n"
            violations_reg.write(line_reg)

            num_violations += 1

    text = "Violaciones de la Distancia de Seguridad: " + \
        str(num_violations / 2)
    cv2.putText(image, text, (10, image.shape[0] - 25),
                cv2.FONT_HERSHEY_COMPLEX, 0.55, (255, 255, 255), 2)

    name = "iteracion_" + str(iteration) + ".png"
    cv2.imwrite(name, image)

    image = cv2.resize(image, (1920, 1080))
    cv2.imshow("Image:", image)
    cv2.waitKey(1)

violations_reg.close()
