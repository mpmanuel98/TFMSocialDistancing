"""
Module azure_faceapi.py.

In this module there are some definitions ir order to send requests to
the Azure Face API cloud service. With that, the user will be able to
create person groups, insert people (previously created) in these
person groups and add faces to each person. After that some tasks like
face detection or face recognition can be performed.
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import json

import requests

"""
Attributes
----------
API Subscription keys.
Endpoint and services URLs.
"""

subscription_key1 = "bbd185d3018149b7bbd5fb2d9e6e937f"
subscription_key2 = "4f002c71a79f46da988bc2ce2105224e"

endpoint = "https://faceiasmarthome.cognitiveservices.azure.com"
faceia_url_persongroups = "/face/v1.0/persongroups/"
faceia_url_detect = "/face/v1.0/detect/"
faceia_url_identify = "/face/v1.0/identify/"

"""
Definitions (functions)
----------
All the functions to make the requests to the Azure Face API
"""

def detect_face(img, detection_model, recognition_model):
    """Detects faces in a given image.

    Parameters
    ----------
    img : Jpeg image data
        The data of the image.
    detection_model : string
        The "detectionModel" associated with the detected faceIds
        ("detection_01" or "detection_02").
    recognition_model : string
        The "recognitionModel" associated with the detected faceIds
        ("recognition_01" or "recognition_02").

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of a detected face.
        {idFace, faceRectangle, age, blur, noise, exposure}
    """

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key1}

    params = {
        "returnFaceId": "true",
        "detectionModel": detection_model,
        "recognitionModel": recognition_model,
        "returnFaceAttributes": "age,blur,exposure,noise"
    }

    url_req = endpoint + faceia_url_detect
    response = requests.post(url=url_req, headers=headers, params=params, data=img)
    response_json = response.json()

    faces_detected = []
    for face in response_json:
        face_item = dict()
        face_item["idFace"] = face.get("faceId")
        face_item["faceRectangle"] = face.get("faceRectangle")
        face_item["age"] = face.get("faceAttributes").get("age")
        face_item["blur"] = face.get("faceAttributes").get("blur").get("value")
        face_item["noise"] = face.get("faceAttributes").get("noise").get("value")
        face_item["exposure"] = face.get("faceAttributes").get("exposure").get("value")

        faces_detected.append(face_item)

    return faces_detected

def identify_face(id_faces, id_group):
    """Indentifies faces in a detected faces list.

    Parameters
    ----------
    id_faces : list
        List of detected faces ids.
    id_group : string
        Group where the identification will be executed.

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of an identified face.
        {idPerson, confidence}
    """

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    body = {
        "faceIds": id_faces,
        "personGroupId": id_group
    }
    body = str(body)

    url_req = endpoint + faceia_url_identify
    response = requests.post(url=url_req, headers=headers, data=body)
    response_json = response.json()

    identified_faces = []
    for detected_face in response_json:
        for candidates in detected_face.get("candidates"):
            face_data = dict()
            face_data["idPerson"] = candidates.get("personId")
            face_data["confidence"] = candidates.get("confidence")

            identified_faces.append(face_data)
    
    return identified_faces

def identify_process(img, id_group, detection_model, recognition_model):
    """Indentifies faces in a given image.

    Parameters
    ----------
    img : Jpeg image data
        The data of the image.
    id_group : string
        Group where the identification will be executed.
    detection_model : string
        The "detectionModel" associated with the detected faceIds
        ("detection_01" or "detection_02").
    recognition_model : string
        The "recognitionModel" associated with the detected faceIds
        ("recognition_01" or "recognition_02").

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of an identified face.
        {idPerson, name, data, confidence}
    """

    detected_faces = detect_face(img, detection_model, recognition_model)

    if detected_faces is None:
        return None

    face_list = []
    for face in detected_faces:
        face_list.append(face.get("idFace"))

    identified_people = identify_face(face_list, id_group)

    if identified_people is None:
        return None

    people = []
    for faces in identified_people:
        person = dict()
        id_person = faces.get("idPerson")
        person_info = get_PGPerson(id_group, id_person)
        person["idPerson"] = id_person
        person["name"] = person_info.get("name")
        person["data"] = person_info.get("data")
        person["confidence"] = faces.get("confidence")

        people.append(person)

    return people

def detect_presence(img, detection_model, recognition_model):
    """Detects if there is a person in the given image.

    Parameters
    ----------
    img : Jpeg image data
        The data of the image.
    detection_model : string
        The "detectionModel" associated with the detected faceIds
        ("detection_01" or "detection_02").
    recognition_model : string
        The "recognitionModel" associated with the detected faceIds
        ("recognition_01" or "recognition_02").

    Returns
    -------
    bool
        True: if there is human presence.
        False: otherwise.
    """

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key1}

    params = {
        "returnFaceId": "true",
        "detectionModel": detection_model,
        "recognitionModel": recognition_model,
        "returnFaceLandmarks": "true",
        "returnFaceAttributes": "age,blur,exposure,noise"
    }

    url_req = endpoint + faceia_url_detect
    response = requests.post(url=url_req, headers=headers, params=params, data=img)

    if(response.text == "[]"):
        return False
    
    return True

# PERSON GROUP

def create_person_group(id_group, name, data, recognition_model):
    """Create a new person group.

    Parameters
    ----------
    id_group : string
        User-provided id of the group to create.
    name : string
        Person group display name.
    data : string
        User-provided data attached to the person group.
    recognition_model : string
        The "recognitionModel" associated with this person group
        ("recognition_01" or "recognition_02").

    Returns
    -------
    int
        Response status code (200 = Success).
    """
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    body = {
        "name": name,
        "userData": data,
        "recognitionModel": recognition_model
    }
    body = str(body)

    url_req = endpoint + faceia_url_persongroups + id_group
    response = requests.put(url=url_req, headers=headers, data=body)
    
    return response.status_code

def delete_person_group(id_group):
    """Delete a person group.

    Parameters
    ----------
    id_group : string
        User-provided id of the group to delete.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group
    response = requests.delete(url=url_req, headers=headers)

    return response.status_code

def get_person_group(id_group, get_model):
    """Gets all the information about a specific person group.

    Parameters
    ----------
    id_group : string
        User-provided id of the group to delete.
    get_model : bool
        Determines whether the group recognition model is
        obtained or not.

    Returns
    -------
    dict
        Dictionary with the information about the person group.
        {idPersonGroup, name, userData, recognitionModel}
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    params = {
        "returnRecognitionModel": get_model
    }

    url_req = endpoint + faceia_url_persongroups + id_group
    response = requests.get(url=url_req, headers=headers, params=params)
    response_json = response.json()

    info_person_group = dict()
    info_person_group["idPersonGroup"] = response_json.get("personGroupId")
    info_person_group["name"] = response_json.get("name")
    info_person_group["userData"] = response_json.get("userData")
    info_person_group["recognitionModel"] = response_json.get("recognitionModel")

    return info_person_group

def list_person_group():
    """Lists all the existing person groups.

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of an existing person group.
        {personGroupId, name, userData}
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups
    response = requests.get(url=url_req, headers=headers)
    response_json = response.json()

    person_group_list = []
    for person_group in response_json:
        person_group_list.append(person_group)

    return person_group_list

def train_person_group(id_group):
    """Trains the specified person group.

    Parameters
    ----------
    id_group : string
        User-provided id of the person group to train.

    Returns
    -------
    int
        Response status code (202 = Success).
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/train"
    response = requests.post(url=url_req, headers=headers)
    
    return response.status_code

def get_training_status(id_group):
    """Gets the training status of the person group.

    Parameters
    ----------
    id_group : string
        User-provided id of the person group to
        obtain the training status.

    Returns
    -------
    dict
        Dictionary with information about the training status.
        {status, createdDateTime, lastActionDateTime, message,
        lastSuccessfulTrainingId, lastSuccessfulTrainingDateTime}
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    params = {
        "returnRecognitionModel"
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/training"
    response = requests.get(url=url_req, headers=headers)
    response_json = response.json()

    info_training_status = dict()
    info_training_status["status"] = response_json["status"]
    info_training_status["createdDateTime"] = response_json["createdDateTime"]
    info_training_status["lastActionDateTime"] = response_json["lastActionDateTime"]
    info_training_status["message"] = response_json["message"]
    info_training_status["lastSuccessfulTrainingId"] = response_json["lastSuccessfulTrainingId"]
    info_training_status["lastSuccessfulTrainingDateTime"] = response_json["lastSuccessfulTrainingDateTime"]

    return info_training_status

# PERSON GROUP PERSON

def create_PGPerson(id_group_dest, name, data):
    """Creates a person in a person group.

    Parameters
    ----------
    id_group_dest : string
        Specifying the target person group to create the person.
    name : string
        Display name of the target person.
    data : string
        User-provided data attached to a person.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    body = {
        "name": name,
        "userData": data
    }
    body = str(body)

    url_req = endpoint + faceia_url_persongroups + id_group_dest + "/persons"
    response = requests.post(url=url_req, headers=headers, data=body)

    return response.status_code

def add_face_PGPerson(id_group, id_person, dir_img, data):
    """Add a face to a person into a person group.

    Parameters
    ----------
    id_group : string
        Specifying the person group containing the target person.
    id_person : string
        Target person id that the face is added to.
    dir_img : string
        Directory where the face image is stored.
    data : string
        User-specified data about the target face

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    params = {
        "userData": data
    }

    body = open(dir_img, "rb").read()

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons/" + id_person + "/persistedFaces"
    response = requests.post(url=url_req, headers=headers, data=body, params=params)
    
    return response.status_code

def delete_PGPerson(id_group, id_person):
    """Delete an existing person from a person group.

    Parameters
    ----------
    id_group : string
        Specifying the person group containing the person to delete.
    id_person : string
        The target person id to delete.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons/" + id_person
    response = requests.delete(url=url_req, headers=headers)

    return response.status_code

def delete_face_PGPerson(id_group, id_person, id_persisted_face):
    """Delete a face from a person in a person group.

    Parameters
    ----------
    id_group : string
        Specifying the person group containing the target person.
    id_person : string
        Specifying the person that the target persisted face belong to.
    id_persisted_face : string
        Specifying the persisted face to remove. 

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons/" + id_person + "/persistedFaces/" + id_persisted_face
    response = requests.delete(url=url_req, headers=headers)

    return response.status_code

def get_PGPerson(id_group, id_person):
    """Gets the information about a specified person
    in a specified person group.

    Parameters
    ----------
    id_group : string
        Specifying the person group containing the target person.
    id_person : string
        Specifying the target person.

    Returns
    -------
    dict
        Dictionary with information about the person
        in the person group.
        {name, data, persistedFaceIds}
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons/" + id_person
    response = requests.get(url=url_req, headers=headers)
    response_json = response.json()
    
    person_info = dict()
    person_info["name"] = response_json["name"]
    person_info["data"] = response_json["userData"]
    person_info["persistedFaceIds"] = response_json["persistedFaceIds"]

    return person_info

def get_face_PGPerson(id_group, id_person, id_persisted_face):
    """Gets person face information.

    Parameters
    ----------
    id_group : string
        Specifying the person group containing the target person.
    id_person : string
        Specifying the target person that the face belongs to.
    id_persisted_face : string
        The id of the target persisted face of the person.

    Returns
    -------
    string
        Data associated to the face specified.
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons/" + id_person + "/persistedFaces/" + id_persisted_face
    response = requests.get(url=url_req, headers=headers)
    response_json = response.json()

    return response_json["userData"]

def list_PGPerson(id_group):
    """Lists all the people information in the specified person group.

    Parameters
    ----------
    id_group : string
        id of the target person group.

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of each person in the speficied person group.
        {personId, persistedFaceIds (list), name, userData}
    """

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key1
    }

    url_req = endpoint + faceia_url_persongroups + id_group + "/persons"
    response = requests.get(url=url_req, headers=headers)
    response_json = response.json()

    person_info = []
    for person in response_json:
        person_info.append(person)

    return person_info
