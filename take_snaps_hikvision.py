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

"""
cv2.imshow("image", image)
cv2.waitKey(1000)
cv2.destroyAllWindows()
"""

cap = cv2.VideoCapture()
cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")

for i in range(1, 100):
    name = "image_hikvision_" + str(i)
    name = name + ".png"

    ret, frame = cap.read()
    # type(frame) -> <class 'numpy.ndarray'>
    cv2.imwrite(name,frame)
    time.sleep(2)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
