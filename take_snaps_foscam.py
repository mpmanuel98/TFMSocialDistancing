import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
#import face_recognition as FR
import requests
import xml.etree.ElementTree as ET
import io
import time
from PIL import Image
#import cv2
import numpy as np

for i in range(1, 100):
    name = "image_foscam_" + str(i)
    name = name + ".png"
    FWC.take_and_save_capture(FWC.url_home_tests, name)
    time.sleep(2)

"""
for i in range(1, 100):
    #Obtenemos un frame de la camara IP
    frame = FWC.take_and_save_snap(FWC.url_home_tests, "imagenes_smarthome/imagen" + str(i) + ".png")
    time.sleep(0.5)
"""