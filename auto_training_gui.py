"""
auto_training_gui.py
-----------------------
"""
__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import os
import shutil
import sys
import time

import cv2
import mysql.connector
import numpy as np
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

"""
Parameters
----------
"""
# define the conector to the mysql db
db_connector = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="tfm_control_aula"
)

# define the db cursor
db_cursor = db_connector.cursor(buffered=True)

# define the total number of images to take
NUM_IMAGES = 5

# define the refresh time (in seconds) between images taken
FREQUENCE = 10 / (NUM_IMAGES)

class dialog_GUI(QDialog):

    def __init__(self, img_name, img_index, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("dialog.ui", self)
        self.image_name = img_name
        self.image_index = img_index

        pixmap = QPixmap("training_images/cropped_temp_faces/" + self.image_name)
        self.image.setPixmap(pixmap)

        for people_dirs in os.listdir("training_images"):

            if(people_dirs == "cropped_temp_faces"):
                continue
            
            # get person name using the ID
            # insert the person in the db
            try:  
                sql = ("SELECT nombre FROM estudiante WHERE dni = %s")
                values = (people_dirs, )
                db_cursor.execute(sql, values)
                myresult = db_cursor.fetchone()
                self.combo_user.addItem(myresult[0], people_dirs)
            except:
                print("Usuario no encontrado.")

        self.image_iteration.setText("Captura #" + str(self.image_index) + " de " + str(len(os.listdir("training_images/cropped_temp_faces/"))))
        self.button_delete.clicked.connect(self.delete_image)
        self.button_select.clicked.connect(self.select_image)
        self.button_add.clicked.connect(self.new_image)

    def select_image(self):
        shutil.move("training_images/cropped_temp_faces/" + self.image_name, "training_images/" + self.combo_user.currentData() + "/" + self.image_name)
        self.close()

    def new_image(self):
        new_name = self.input_username.text()
        new_id = self.input_userid.text()

        # insert the person in the db
        try:  
            sql = "INSERT INTO estudiante (dni, nombre) VALUES (%s, %s)"
            values = (new_id, new_name)

            db_cursor.execute(sql, values)
            db_connector.commit()

            if(db_cursor.rowcount == 1):
                print("1 person inserted in the DB.")
        except:
            print("Person already inserted in the DB with the provided ID.")

        if not os.path.exists("training_images/" + new_id):
            os.makedirs("training_images/" + new_id)

        shutil.move("training_images/cropped_temp_faces/" + self.image_name, "training_images/" + new_id + "/" + self.image_name)
        self.close()

    def delete_image(self):
        os.remove("training_images/cropped_temp_faces/" + self.image_name)
        self.close()

class main_GUI(QMainWindow):

    # define the default camera to use (hikvision | foscam)
    CAMERA = "hikvision"

    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.estado_capturas.setText("Sin obtener.")
        self.estado_clasificacion.setText("Sin realizar.")
        self.boton_entrenamiento.clicked.connect(self.capture_images)
        self.boton_clasificacion.clicked.connect(self.classify_images)
        self.radio_foscam.clicked.connect(self.select_foscam)
        self.radio_hikvision.clicked.connect(self.select_hikvision)

    def select_hikvision(self):
        self.CAMERA = "hikvision"

    def select_foscam(self):
        self.CAMERA = "foscam"

    def capture_images(self):
        if not os.path.exists("training_images/cropped_temp_faces"):
            os.makedirs("training_images/cropped_temp_faces")

        print("Starting the general face detection process...")
        self.estado_capturas.setText("En proceso...")

        face_id = 0
        for iteration in range(0, NUM_IMAGES):
            # take a capture from the IP camera
            if(self.CAMERA == "foscam"):
                img = FWC.take_capture("http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?")
                pil_image = Image.open(io.BytesIO(img))
                image = np.array(pil_image)
            elif(self.CAMERA == "hikvision"):
                cap = cv2.VideoCapture()
                cap.open("rtsp://admin:AmgCam18*@192.168.1.51:554/Streaming/Channels/1")
                ret, image = cap.read()
            else:
                exit()

            imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(imageRGB)

            # detect faces in the capture taken
            faces = OFP.detect_faces(image, 150)

            if faces is None:
                continue

            # save the cropped face in a temporary directory
            for face in faces:
                x, y, w, h = face
                pil_img = pil_img.crop((x, y, x+w, y+h))
                pil_img.save("training_images/cropped_temp_faces/image_" + str(face_id) + ".png")
                face_id += 1
            
            print("Captures taken and saved!")
            time.sleep(FREQUENCE)

        self.estado_capturas.setText("Obtenidas.")
        print("General face detection process finished.")

    def classify_images(self):
        print("Starting the classification process...")
        self.estado_clasificacion.setText("En proceso...")

        img_index = 1
        for image_name in os.listdir("training_images/cropped_temp_faces"):
            dlg = dialog_GUI(image_name, img_index)
            img_index += 1
            dlg.exec()

        self.estado_clasificacion.setText("Realizado.")
        print("Classification process finished. Exiting...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = main_GUI()
    GUI.show()
    sys.exit(app.exec_())
