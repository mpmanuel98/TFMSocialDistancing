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
from urllib.request import urlopen
import cv2
import numpy as np
from PIL import Image

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

stream = urlopen("http://192.168.1.149:81/stream")
bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        if jpg :
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("Image:", img)
            cv2.waitKey(5)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()



