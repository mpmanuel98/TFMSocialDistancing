"""
Script auto_training_gui.py
-----------------------

This script is used to perform a supervised training using
a graphical interface.
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
Minimum size (in pixels) of a face to be detected.
Margin (in pixels) around the detected faces.
Connector to the MySQL database.
"""
# define the minimum size (in pixels) of a face to be detected
FACE_MIN_SIZE = 30

# define the margin (in pixels) around detected faces
FACE_MARGIN = 25

# define the conector to the mysql db
db_connector = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="tfm_control_aula"
)

# define the db cursor
db_cursor = db_connector.cursor(buffered=True)

"""
Classes
----------
"""
class dialog_GUI(QDialog):

    def __init__(self, img_name, img_index, parent=None):
        """Initialize the dialog_GUI class.

        Parameters
        ----------
        img_name : string
            Name of the image to process.
        img_index : int
            Index of the image to process.
        parent : None
        """
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("gui/dialog.ui", self)
        self.image_name = img_name
        self.image_index = img_index

        pixmap = QPixmap("training_images/cropped_temp_faces/" + self.image_name)
        self.image.setPixmap(pixmap)

        for people_dirs in os.listdir("training_images"):

            if(people_dirs == "cropped_temp_faces"):
                continue
            
            # get person name using the ID
            try:  
                sql = ("SELECT nombre FROM estudiante WHERE dni = %s")
                values = (people_dirs, )
                db_cursor.execute(sql, values)
                myresult = db_cursor.fetchone()
                self.combo_user.addItem(myresult[0], people_dirs)
            except:
                print("Usuario no encontrado.")

        self.image_iteration.setText("Captura #" + str(self.image_index) + " de " + str(len(os.listdir("training_images/cropped_temp_faces/"))))
        self.button_select.clicked.connect(self.select_image)
        self.button_add.clicked.connect(self.new_image)
        self.button_delete.clicked.connect(self.delete_image)

    def select_image(self):
        """Move the temp image to the directory of
        the person already registered.
        """
        shutil.move("training_images/cropped_temp_faces/" + self.image_name, "training_images/" + self.combo_user.currentData() + "/" + self.image_name)
        self.close()

    def new_image(self):
        """Move the temp image to a new directory of
        the person to register.
        """
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
        """Delete the temp image.
        """
        os.remove("training_images/cropped_temp_faces/" + self.image_name)
        self.close()

class main_GUI(QMainWindow):

    # define the default camera to use (hikvision | foscam)
    CAMERA = "hikvision"

    def __init__(self):
        """Initialize the main_GUI class.
        """
        super().__init__()
        uic.loadUi("gui/main.ui", self)

        self.estado_capturas.setText("Estado: Pendiente.")
        self.estado_clasificacion.setText("Estado: Pendiente.")
        self.boton_entrenamiento.clicked.connect(self.capture_images)
        self.boton_clasificacion.clicked.connect(self.classify_images)
        self.radio_foscam.clicked.connect(self.select_foscam)
        self.radio_hikvision.clicked.connect(self.select_hikvision)

    def select_hikvision(self):
        """Select the Hikvision camera model.
        """
        self.CAMERA = "hikvision"

    def select_foscam(self):
        """Select the Foscam camera model.
        """
        self.CAMERA = "foscam"

    def capture_images(self):
        """Sub-process to capture images from
        the IP camera.
        """
        if not os.path.exists("training_images/cropped_temp_faces"):
            os.makedirs("training_images/cropped_temp_faces")

        print("Starting the general face detection process...")
        self.estado_capturas.setText("Estado: En proceso...")

        num_images = int(self.spin_num_capturas.value())
        frequence = (float(self.spin_tiempo.value()) * 60) / (num_images)

        face_id = 0
        for iteration in range(0, num_images):
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

            # detect faces in the capture taken
            faces = OFP.detect_faces(image, FACE_MIN_SIZE)

            if faces is None:
                continue

            # save the cropped face in a temporary directory
            for face in faces:
                x, y, w, h = face
                        
                #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
                face_cropped = image[(y - FACE_MARGIN):(y + h + FACE_MARGIN), (x - FACE_MARGIN):(x + w + FACE_MARGIN)]
                cv2.imwrite("training_images/cropped_temp_faces/image_" + str(face_id) + ".png", face_cropped)
                
                face_id += 1
            
            cv2.imwrite("test.png", image)
            cv2.waitKey(0)

            print("Captures taken and saved!")
            time.sleep(frequence)

        self.estado_capturas.setText("Estado: Finalizado.")
        print("General face detection process finished.")

    def classify_images(self):
        """Sub-process to classify the captures taken.
        """
        print("Starting the classification process...")
        self.estado_clasificacion.setText("Estado: En proceso...")

        # for each image taken, opens a dialog to classify it
        img_index = 1
        for image_name in os.listdir("training_images/cropped_temp_faces"):
            dlg = dialog_GUI(image_name, img_index)
            img_index += 1
            dlg.exec()

        self.estado_clasificacion.setText("Estado: Finalizado.")
        print("Classification process finished. Exiting...")

"""
Script
----------
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = main_GUI()
    GUI.show()
    sys.exit(app.exec_())
