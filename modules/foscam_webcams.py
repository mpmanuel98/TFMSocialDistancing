"""
Module foscam_webcams.py.

In this module there are some definitions ir order to send requests to
the Foscam IP cameras installed on the smart home. With that, the user 
will be able to move the cameras, move to a preset point, zoom in,
zoom out and take snaps.
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import xml.etree.ElementTree as ET

import requests
from PIL import Image

"""
Attributes
----------
Authentication credentials.
Access URLs to the cameras.
Dictionaries with the requests parameters.
"""

user = "admin"
password = "AmgCam18*"

url_living_room = "http://192.168.7.225:8894/cgi-bin/CGIProxy.fcgi?"
url_distributor = "http://192.168.7.224:8893/cgi-bin/CGIProxy.fcgi?"
url_kitchen = "http://192.168.7.223:8892/cgi-bin/CGIProxy.fcgi?"
url_bedroom = "http://192.168.7.222:8891/cgi-bin/CGIProxy.fcgi?"
url_home_tests = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

params_zoom_in = {
    "usr": user,
    "pwd": password,
    "cmd": "zoomIn"
}

params_zoom_out = {
    "usr": user,
    "pwd": password,
    "cmd": "zoomOut"
}

params_zoom_stop = {
    "usr": user,
    "pwd": password,
    "cmd": "zoomStop"
}

params_movement_stop = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzStopRun"
}

params_move_up = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveUp"
}

params_move_down = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveDown"
}

params_move_left = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveLeft"
}

params_move_right = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveRight"
}

params_move_top_left = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveTopLeft"
}

params_move_top_right = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveTopRight"
}

params_move_bottom_left = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveBottomLeft"
}

params_move_bottom_right = {
    "usr": user,
    "pwd": password,
    "cmd": "ptzMoveBottomRight"
}

params_dev_state = {
    "usr": user,
    "pwd": password,
    "cmd": "getDevState"
}

params_get_config_motion_detect = {
    "usr": user,
    "pwd": password,
    "cmd": "getMotionDetectConfig1"
}

params_take_snap = {
    "usr": user,
    "pwd": password,
    "cmd": "snapPicture2"
}

"""
Definitions (functions)
----------
"""

def get_motion_detection_alarm(camera_url):
    """Gets the motion detection alarm.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Motion detection disabled
        1: No movement detected
        2: Movement detected
    """

    response = requests.get(camera_url, params=params_dev_state)
    response_xml = ET.fromstring(response.text)
    motion_detect_alarm = int(response_xml[2].text)

    return motion_detect_alarm

def zoom_in(camera_url):
    """Zooms into the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_zoom_in)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def zoom_out(camera_url):
    """Zooms out on the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_zoom_out)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def zoom_stop(camera_url):
    """Stops zooming on the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_zoom_stop)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def movement_stop(camera_url):
    """Stops the movement on the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_movement_stop)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_up(camera_url):
    """Moves up the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_up)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_down(camera_url):
    """Moves down the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_down)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_left(camera_url):
    """Moves the specified camera to the left.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_left)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_right(camera_url):
    """Moves the specified camera to the right.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_right)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_top_left(camera_url):
    """Moves the specified camera to the top-left position.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_top_left)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_top_right(camera_url):
    """Moves the specified camera to the top-right position.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_top_right)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_bottom_left(camera_url):
    """Moves the specified camera to the bottom-left position.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_bottom_left)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_bottom_right(camera_url):
    """Moves the specified camera to the bottom-right position.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    response = requests.get(camera_url, params=params_move_bottom_right)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def move_preset_point(camera_url, preset_point):
    """Moves the specified camera to a specified preset point.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.
    preset_point : string
        Destination preset point.

    Returns
    -------
    int
        0: Success.
        -1: Error.
    """

    params_move_preset_point = {"usr": user,
                                "pwd": password,
                                "cmd": "ptzGotoPresetPoint",
                                "name": preset_point
                                }

    response = requests.get(camera_url, params=params_move_preset_point)
    response_xml = ET.fromstring(response.text)
    status_code = int(response_xml[0].text)

    return status_code

def take_capture(camera_url):
    """Takes a capture on the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.

    Returns
    -------
    Jpeg image data
        Data corresponding to the capture taken.
    """

    response = requests.get(camera_url, params=params_take_snap)

    return response.content

def take_and_save_capture(camera_url, dir_dest):
    """Takes and saves a capture on the specified camera.

    Parameters
    ----------
    camera_url : string
        URL of the source camera.
    dir_dest : string
        Directory where the capture will be saved.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    # type(response.content) -> <class 'bytes'>
    # type(io.BytesIO(response.content)) -> <class '_io.BytesIO'>
    # type(pil_image) -> <class 'PIL.JpegImagePlugin.JpegImageFile'>

    response = requests.get(camera_url, params=params_take_snap)    
    pil_image = Image.open(io.BytesIO(response.content))
    pil_image.save(dir_dest)

    return response.status_code
