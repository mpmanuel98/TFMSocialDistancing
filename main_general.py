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
MIN_DISTANCE = 100

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
        cv2.imshow("Image Cropped:", face.get("face_cropped"))

        x, y, w, h = face.get("coords")
        centroid = (int((x+(x+w))/2), int((y+(y+h))/2))
        centroids.append(centroid)
        cv2.circle(image, centroid, radius=0, color=(0, 255, 0), thickness=10)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    D = dist.cdist(centroids, centroids, metric="euclidean")

    violate = set()
    # loop over the upper triangular of the distance matrix
    for i in range(0, D.shape[0]):
        for j in range(i + 1, D.shape[1]):
            # check to see if the distance between any two
            # centroid pairs is less than the configured number
            # of pixels
            if D[i, j] < MIN_DISTANCE:
                # update our violation set with the indexes of
                # the centroid pairs
                violate.add(i)
                violate.add(j)

    cv2.imshow("Image Delimited:", image)
    cv2.waitKey(1)

    time.sleep(1)
