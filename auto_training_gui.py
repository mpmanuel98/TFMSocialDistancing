"""
Script auto_training.py
-----------------------
"""
__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import os
import shutil
import time
from tkinter import *
from tkinter.ttk import *

import cv2
import mysql.connector
from PIL import Image
import numpy as np

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

def select_hikvision():
    global CAMERA 
    CAMERA = "hikvision"
    print(CAMERA)

def select_foscam():
    global CAMERA 
    CAMERA = "foscam"
    print(CAMERA)

def capture_images():
    if not os.path.exists("training_images/cropped_temp_faces"):
        os.makedirs("training_images/cropped_temp_faces")

    print("Starting the general face detection process...")
    label1.configure(text= "En proceso...")

    face_id = 0
    for iteration in range(0, NUM_IMAGES):
        # take a capture from the IP camera
        if(CAMERA == "foscam"):
            img = FWC.take_capture("http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?")
            pil_image = Image.open(io.BytesIO(img))
            image = np.array(pil_image)
        elif(CAMERA == "hikvision"):
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

    label1.configure(text= "Capturas tomadas.")
    print("General face detection process finished.")

"""
Script
------
"""

window = Tk()
window.title("Proceso de Entrenamiento Supervisado")
window.geometry("1200x800")

label = Label(window, text="Entrenamiento supervisado")
label.grid(column=0, row=0)
label.config(anchor=CENTER)

label1 = Label(window, text="Estado: Capturas sin tomar.")
label1.grid(column=0, row=1)

rad1 = Radiobutton(window,text="Hikvision 4K", value="hikvision", command=select_hikvision)
rad2 = Radiobutton(window,text="Foscam", value="foscam", command=select_foscam)
rad1.grid(column=0, row=2)
rad2.grid(column=1, row=2)

btn = Button(window, text="Capturar imagenes", command=capture_images)

btn.grid(column=0, row=3)

window.mainloop()



print("Starting the classification process...")

for image_name in os.listdir("training_images/cropped_temp_faces"):

    image = cv2.imread("training_images/cropped_temp_faces/" + image_name)

    # show the capture taken to the user
    cv2.imshow("Press any key to start the classification...", image)
    cv2.waitKey(0)

    print("\nOptions list:\n")
    people_indexes = dict()
    index = 1
    for people_dirs in os.listdir("training_images"):

        if(people_dirs == "cropped_temp_faces"):
            continue
        
        # get person name using the ID
        sql = ("SELECT nombre FROM estudiante WHERE dni = %s")
        values = (people_dirs, )
        db_cursor.execute(sql, values)
        myresult = db_cursor.fetchone()
        
        print(str(index) + " -> " + myresult[0])
        people_indexes[index] = people_dirs

        index += 1

    people_indexes[index] = "new"
    print(str(index) + " -> Add new person")
    index += 1
    people_indexes[index] = "none"
    print(str(index) + " -> Remove image")

    value_selected = input("\nWho is this person? (select an option from above): ")

    if(int(value_selected) == int(len(people_indexes) - 1)):

        new_name = input("\nInsert the name of the new person: ")
        new_id = input("\nInsert the ID of the new person: ")

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

        shutil.move("training_images/cropped_temp_faces/" + image_name, "training_images/" + new_id + "/" + image_name)
    elif(int(value_selected) == int(len(people_indexes))):
        os.remove("training_images/cropped_temp_faces/" + image_name)
    else:
        shutil.move("training_images/cropped_temp_faces/" + image_name, "training_images/" + people_indexes.get(int(value_selected)) + "/" + image_name)

print("Classification process finished. Exiting...")
