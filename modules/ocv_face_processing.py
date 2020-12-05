"""
Module ocv_face_processing.py.

In this module there are some definitions ir order to detect faces and
to create the necessary structures to make the subsequent face
recognition. Also, there is a Class to create Recognizer instances using
a specified algorithm. For all the face processes OpenCV algorithms
are used.

Also some functions are defined:
    detect_frontal_faces(img)
    create_recognition_structures(training_images_path)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import os

import cv2
import numpy as np

"""
Definitions (functions)
----------
"""

def detect_frontal_faces(img):
    """Detects faces in a given image.

    Parameters
    ----------
    img : Jpeg image data
        Data corresponding to the image where faces are being detected.

    Returns
    -------
    list
        List of cropped and scaled images with the region of the
        detected faces.
    """
    # Ecualizacion del histograma (para suavizar los cambios de iluminacion)
    # equ = cv2.equalizeHist(img)

    # Aplicando filtro bilatreal para realizar un suavizado de la imagen
    #blur = cv2.bilateralFilter(equ,9,75,75)

    # Haar Classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")

    faces_detected = face_cascade.detectMultiScale(img, scaleFactor=1.1)

    if (len(faces_detected) == 0):
        return None

    faces = []

    for face in faces_detected:
        face_info = dict()
        x, y, w, h = face

        cropped_scaled_face = cv2.resize(img[y:y+h, x:x+w], (200, 200))

        face_info["face_cropped"] = cropped_scaled_face
        face_info["coords"] = face

        faces.append(face_info)

    return faces

def create_recognition_structures(training_images_path):
    """Creates the structures necessary to make the subsequent
    face recognition.

    Parameters
    ----------
    training_images_path : string
        Path to the directory where the training images are saved.

    Returns
    -------
    list
        List of cropped and scaled images with the region of the
        detected faces in the training samples.
    list
        List of integers which represents the label of each image
        saved in the first returned list.
    dict
        Dictionary that contains the relation between the labels 
        of the second returned list with the names of the people.
    """

    faces = []
    labels = []
    subject_names = dict()
    subject_index = 0
    directories = os.listdir(training_images_path)

    for dir_name in directories:

        subject_names[subject_index] = dir_name

        subject_dir_path = training_images_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            
            print("Processing the image: ", image_name)

            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            detected_faces = detect_frontal_faces(image)

            if detected_faces is None:
                continue

            for face in detected_faces:
                faces.append(face.get("face_cropped"))
                labels.append(subject_index)

        subject_index += 1            

    return faces, labels, subject_names

"""
Classes
----------
"""

class Recognizer:
    """
    A class used to represent a face recognizer.

    Attributes
    ----------
    recognizer : openCV.recognizer
        The openCV face recognizer that is going to be used.
    faces : list
        List of cropped and scaled images with the region of the
        detected faces in the training samples.
    labels : list
        List of integers which represents the label of each image
        saved in the first returned list.
    names : dict
        Dictionary that contains the relation between the labels 
        of the second returned list with the names of the people.

    Methods
    -------
    __init__(recognizer, faces, labels, names)
        Initialize an instance of the class.
    predict(img)
        Tries to recognize a person in the given image.
    """
    
    recognizer = None
    faces=[]
    labels=[]
    names=dict()

    def __init__(self, recognizer, faces, labels, names):
        """
        Parameters
        ----------
        recognizer : string
            The openCV face recognizer that is going to be used.
        faces : list
            List of cropped and scaled images with the region of the
            detected faces in the training samples.
        labels : list
            List of integers which represents the label of each image
            saved in the first returned list.
        names : dict
            Dictionary that contains the relation between the labels 
            of the second returned list with the names of the people.
        """

        self.names = names

        if(recognizer == "eigenfaces"):
            self.recognizer = cv2.face.EigenFaceRecognizer_create()
        elif(recognizer == "fisherfaces"):
            self.recognizer = cv2.face.FisherFaceRecognizer_create()
        else:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            
        self.recognizer.train(faces, np.array(labels))   

    def predict(self, img):
        """Tries to recognize a person in the given image.

        Parameters
        ----------
        img : Jpeg image data
            Data corresponding to the image where faces are being
            recognized.

        Returns
        -------
        list
            List with the name and the confidence of the people
            recognized.
        """

        face_list = detect_frontal_faces(img)

        if face_list is None:
            return None

        people_identified = []

        for face in face_list:

            info_recognizer = self.recognizer.predict(face.get("face_cropped"))

            person = []
            label_text = self.names.get(info_recognizer[0])
            person.append(label_text)
            person.append(info_recognizer[1])

            people_identified.append(person)

        return people_identified