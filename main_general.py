"""
Script main_general.py.

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

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

# define the minimum safe distance (in pixels) that two people can be from each other
MIN_DISTANCE = 1500

# define the relation between pixels and cms (pixels, cms)
RELATION = (30, 3)

"""
Script
----------
"""

while True:
    img = FWC.take_capture(FWC.url_home_tests)
    pil_image = Image.open(io.BytesIO(img))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    faces = OFP.detect_faces(image)

    if faces is None:
        continue

    centroids = []
    #face_index = 0
    for face in faces:
        x, y, w, h = face

        # save the cropped face in the corresponding directory
        """
        filename = time.strftime("%d_%m_%Y-%H.%M.%S") + ".jpg"
        cv2.imwrite(str(face_index) + "/" + filename, face.get("face_cropped"))
        """

        # compute and store the centroids of the faces detected
        centroid = (int((x+(x+w))/2), int((y+(y+h))/2))
        centroids.append(centroid)

        # plot the centroid and the rectangle arround the faces
        cv2.circle(image, centroid, radius=0, color=(0, 255, 0), thickness=3)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

        #face_index += 1

    # compute the euclidean distance between the centroids
    dist_comp = dist.cdist(centroids, centroids, metric="euclidean")

    violates = dict()
    for i in range(0, dist_comp.shape[0]):
        relations = []
        for j in range(0, dist_comp.shape[1]):

            # check if the distance between two centroid pairs is less than the threshold
            if (dist_comp[i, j] < MIN_DISTANCE) and (dist_comp[i, j] > 0):
                relations.append((centroids[j], dist_comp[i, j]))

        if len(relations) == 0:
            continue

        violates[centroids[i]] = relations

    num_violates = 0
    for key, value in violates.items():
        for rel_tuple in value:

            cv2.line(image, key, rel_tuple[0],
                     (0, 0, 255), thickness=1, lineType=8)

            midPoint = (int((key[0] + rel_tuple[0][0]) / 2),
                        int((key[1] + rel_tuple[0][1]) / 2))

            real_distance = rel_tuple[1] * RELATION[1] / RELATION[0]

            cv2.putText(image, str(round(real_distance, 2)) + "cm", midPoint,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            num_violates += 1

    text = "Violaciones de la Distancia de Seguridad: " + str(num_violates / 2)
    cv2.putText(image, text, (10, image.shape[0] - 25),
                cv2.FONT_HERSHEY_COMPLEX, 0.55, (255, 255, 255), 2)

    cv2.imshow("Image:", image)
    cv2.waitKey(1)

    time.sleep(2)
