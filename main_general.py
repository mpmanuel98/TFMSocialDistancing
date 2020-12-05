"""
Script main_general.py.

Description

Also a function is defined:
    function(variable)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import time
import io

from scipy.spatial import distance as dist
import cv2
import numpy as np
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

# define the minimum safe distance (in pixels) that two people can be from each other
MIN_DISTANCE = 300

"""
Script
----------
"""

while True:
    img = FWC.take_capture(FWC.url_home_tests)

    pil_image = Image.open(io.BytesIO(img))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    faces = OFP.detect_frontal_faces(image)

    if faces is None:
        continue

    centroids = []
    for face in faces:
        x, y, w, h = face.get("coords")

        # compute and save the centroids of the faces detected
        centroid = (int((x+(x+w))/2), int((y+(y+h))/2))
        centroids.append(centroid)

        # plot the centroid and the rectangle arround the faces
        cv2.circle(image, centroid, radius=0, color=(0, 255, 0), thickness=10)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    dist_comp = dist.cdist(centroids, centroids, metric="euclidean")

    violates = dict()

    for i in range(0, dist_comp.shape[0]):
        relations = []
        for j in range(0, dist_comp.shape[1]):
            # check if the distance between two centroid pairs is less than the threshold
            print(dist_comp[i, j])
            if dist_comp[i, j] < MIN_DISTANCE and i != j:
                relations.append(j)
        
        violates[i] = relations

    print(violates)
    cv2.imshow("Image Delimited:", image)
    cv2.waitKey(1)

    time.sleep(1)
