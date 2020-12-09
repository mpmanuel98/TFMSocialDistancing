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

# rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/101

cap = cv2.VideoCapture()
cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")

while(True):

    ret, frame = cap.read()
    imS = cv2.resize(frame, (1920, 1080)) 
    cv2.imshow('Stream IP Camera OpenCV',imS)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
