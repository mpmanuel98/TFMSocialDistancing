import cv2
import modules.ocv_face_processing as OFP
import numpy as np
from PIL import Image

pil_image = Image.open("C:/Users/mpman/Desktop/243543W.jpg")
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

faces = OFP.detect_faces(image)

for face in faces:
    x, y, w, h = face
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Image:", image)
cv2.waitKey(100000)
