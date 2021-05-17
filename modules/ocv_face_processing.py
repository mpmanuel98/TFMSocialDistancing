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
import time
import cv2
import numpy as np

"""
Definitions (functions)
----------
"""

def detect_faces(image, min_size):
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
    """
    haarcascade_frontalface_default.xml
    haarcascade_frontalface_alt.xm
    haarcascade_frontalface_alt2.xml
    haarcascade_frontalface_alt_tree.xml
    """
    haar_frontalface = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    haar_profileface = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

    frontal_faces = haar_frontalface.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5, minSize=(min_size,min_size))
    profile_faces = haar_profileface.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5, minSize=(min_size,min_size))

    if (len(frontal_faces) == 0) and (len(profile_faces) == 0):
        return None

    faces_detected = []
    faces_aux = []
        
    if (len(frontal_faces) != 0) and (len(profile_faces) == 0):
        for face in frontal_faces:
            x, y, w, h = face
            faces_aux.append([x, y, w, h])

    if (len(frontal_faces) == 0) and (len(profile_faces) != 0):
        for face in profile_faces:
            x, y, w, h = face
            faces_aux.append([x, y, w, h])

    if (len(frontal_faces) != 0) and (len(profile_faces) != 0):
        for face in frontal_faces:
            x, y, w, h = face
            faces_aux.append([x, y, w, h])

        for face in profile_faces:
            x, y, w, h = face
            faces_aux.append([x, y, w, h])

    faces_aux.extend(faces_aux)
    faces_detected, weights = cv2.groupRectangles(np.array(faces_aux).tolist(), 1, 0.50)

    return faces_detected
 

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
        if(dir_name == "cropped_temp_faces" or dir_name == "backup"):
            continue
        
        subject_names[subject_index] = dir_name

        subject_dir_path = training_images_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            
            print("Processing the image: ", image_name)

            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            detected_faces = detect_faces(image_gray, 150)

            if detected_faces is None:
                print("No face here")
                continue

            for face in detected_faces:
                x, y, w, h = face
                face_cropped = image_gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_cropped, (200, 200))

                faces.append(face_resized)
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

    def identify_single_face(self, image):
        """Identify a face in a given cropped image.

        Parameters
        ----------
        img : Jpeg image data
            Data corresponding to the single cropped face image.

        Returns
        -------
        list
            List with the name and the confidence of the person recognized.
        """

        face_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        face_resized = cv2.resize(face_gray, (200, 200))

        info_recognizer = self.recognizer.predict(face_resized)

        person = []
        label_text = self.names.get(info_recognizer[0])
        person.append(label_text)
        person.append(info_recognizer[1])

        return person


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

        face_list = detect_faces(img, 150)

        if face_list is None:
            return None

        people_identified = []

        for face in face_list:
            x, y, w, h = face
            face_cropped = img[y:y+h, x:x+w]
            face_resized = cv2.resize(face_cropped, (200, 200))

            info_recognizer = self.recognizer.predict(face_resized)

            person = []
            label_text = self.names.get(info_recognizer[0])
            person.append(label_text)
            person.append(info_recognizer[1])

            people_identified.append(person)

        return people_identified