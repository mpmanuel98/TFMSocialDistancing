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

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP


pil_image = Image.open("C:/Users/mpman/Desktop/243543W.jpg")
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

faces = OFP.detect_faces(image)

for face in faces:
    x, y, w, h = face
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Image:", image)
cv2.waitKey(100000)
