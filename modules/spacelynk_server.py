"""
Module spacelynk_server.py.

In this module there are some definitions ir order to send requests to
the spaceLYnk server installed on the smart home. With that, the user 
will be able to control the lights, blinds and curtains. Also some
information from sensors can be obtained.
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import xml.etree.ElementTree as ET

import requests

"""
Attributes
----------
Access URL to the spaceLYnk server.
Dictionaries with the requests parameters.
"""

url_spaceLYnk = "http://admin:amgingenieros@192.168.7.210/scada-remote?"

# Lights

params_kitchen_lights_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "1/1/7"
}

params_kitchen_lights_on = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/7",
    "value": "true"
}

params_kitchen_lights_off = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/7",
    "value": "false"
}

params_bathroom_lights_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    #"alias": "1/1/13" # Mirror light
    "alias": "1/1/11"
}

params_bathroom_lights_on = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    #"alias": "1/1/13", # Mirror light
    "alias": "1/1/11",
    "value": "true"
}

params_bathroom_lights_off = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    #"alias": "1/1/13", # Mirror light
    "alias": "1/1/11",
    "value": "false"
}

params_bedroom_lights_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "1/1/17"
}

params_bedroom_lights_on = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/17",
    "value": "true"
}

params_bedroom_lights_off = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/17",
    "value": "false"
}

params_distributor_lights_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "1/1/5"
}

params_distributor_lights_on = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/5",
    "value": "true"
}

params_distributor_lights_off = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/5",
    "value": "false"
}

params_livroom_lights_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "1/1/15"
}

params_livroom_lights_on = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/15",
    "value": "true"
}

params_livroom_lights_off = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "1/1/15",
    "value": "false"
}

# Blinds

params_kitchen_blind_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/1/4"
}

params_kitchen_blind_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/4",
    "value": "0"
}

params_kitchen_blind_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/4",
    "value": "100"
}

params_bathroom_blind_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/1/8"
}

params_bathroom_blind_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/8",
    "value": "0"
}

params_bathroom_blind_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/8",
    "value": "100"
}

params_bedroom_blind_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/1/12"
}

params_bedroom_blind_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/12",
    "value": "0"
}

params_bedroom_blind_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/1/12",
    "value": "100"
}

# Curtains

params_bedroom_curtain_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/3/8"
}

params_bedroom_curtain_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/8",
    "value": "0"
}

params_bedroom_curtain_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/8",
    "value": "100"
}

params_livroom_curtain_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/3/4"
}

params_livroom_curtain_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/4",
    "value": "0"
}

params_livroom_curtain_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/4",
    "value": "100"
}

params_class_curtain_status = {
    "m": "xml",
    "r": "grp",    
    "fn": "getvalue",
    "alias": "2/3/12"
}

params_class_curtain_up = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/12",
    "value": "0"
}

params_class_curtain_down = {
    "m": "xml",
    "r": "grp",
    "fn": "write",
    "alias": "2/3/12",
    "value": "100"
}

# Information from sensors

params_get_radiation_level = {
    "m": "xml",
    "r": "grp",
    "fn": "getvalue",
    "alias": "3/2/6",
}

params_rain_status = {
    "m": "xml",
    "r": "grp",
    "fn": "getvalue",
    "alias": "3/2/10"
}

params_wind_speed = {
    "m": "xml",
    "r": "grp",
    "fn": "getvalue",
    "alias": "3/2/4"
}

"""
Definitions (functions)
----------
"""

# Lights

def get_kitchen_lights_status():
    """Gets the kitchen lights status.

    Returns
    -------
    bool
        True: Lights on.
        False: Lights off.
    """

    response = requests.get(url_spaceLYnk, params=params_kitchen_lights_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def kitchen_lights_on():
    """Turns the kitchen lights on.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    
    response = requests.get(url_spaceLYnk, params=params_kitchen_lights_on)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def kitchen_lights_off():
    """Turns the kitchen lights off.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_kitchen_lights_off)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_bathroom_lights_status():
    """Gets the bathroom lights status.

    Returns
    -------
    bool
        True: Lights on.
        False: Lights off.
    """

    response = requests.get(url_spaceLYnk, params=params_bathroom_lights_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bathroom_lights_on():
    """Turns the bathroom lights on.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    
    response = requests.get(url_spaceLYnk, params=params_bathroom_lights_on)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bathroom_lights_off():
    """Turns the bathroom lights off.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bathroom_lights_off)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_bedroom_lights_status():
    """Gets the bedroom lights status.

    Returns
    -------
    bool
        True: Lights on.
        False: Lights off.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_lights_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bedroom_lights_on():
    """Turns the bedroom lights on.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_lights_on)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bedroom_lights_off():
    """Turns the bedroom lights off.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_lights_off)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_distributor_lights_status():
    """Gets the distributor lights status.

    Returns
    -------
    bool
        True: Lights on.
        False: Lights off.
    """

    response = requests.get(url_spaceLYnk, params=params_distributor_lights_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def distributor_lights_on():
    """Turns the distributor lights on.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_distributor_lights_on)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def distributor_lights_off():
    """Turns the distributor lights off.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_distributor_lights_off)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_livroom_lights_status():
    """Gets the living room lights status.

    Returns
    -------
    bool
        True: Lights on.
        False: Lights off.
    """

    response = requests.get(url_spaceLYnk, params=params_livroom_lights_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def livroom_lights_on():
    """Turns the living room lights on.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_livroom_lights_on)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def livroom_lights_off():
    """Turns the living room lights off.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_livroom_lights_off)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

# Blinds

def get_kitchen_blind_status():
    """Gets the kitchen blind status.

    Returns
    -------
    int
        Level (100: blind down; 0: blind up).
    """

    response = requests.get(url_spaceLYnk, params=params_kitchen_blind_status)
    response_xml = ET.fromstring(response.text)
    kitchen_blind_status = int(response_xml.text)

    return kitchen_blind_status

def kitchen_blind_up():
    """Raises the kitchen blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_kitchen_blind_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def kitchen_blind_down():
    """Rolls down the kitchen blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    response = requests.get(url_spaceLYnk, params=params_kitchen_blind_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_bathroom_blind_status():
    """Gets the bathroom blind status.

    Returns
    -------
    int
        Level (100: blind down; 0: blind up).
    """

    response = requests.get(url_spaceLYnk, params=params_bathroom_blind_status)
    response_xml = ET.fromstring(response.text)
    bathroom_blind_status = int(response_xml.text)

    return bathroom_blind_status

def bathroom_blind_up():
    """Raises the bathroom blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    response = requests.get(url_spaceLYnk, params=params_bathroom_blind_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bathroom_blind_down():
    """Rolls down the bathroom blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bathroom_blind_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_bedroom_blind_status():
    """Gets the bedroom blind status.

    Returns
    -------
    int
        Level (100: blind down; 0: blind up).
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_blind_status)
    response_xml = ET.fromstring(response.text)
    bedroom_blind_status = int(response_xml.text)

    return bedroom_blind_status

def bedroom_blind_up():
    """Raises the bedroom blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_blind_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bedroom_blind_down():
    """Rolls down the bedroom blind.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_blind_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

# Curtains

def get_bedroom_curtain_status():
    """Gets the bedroom curtain status.

    Returns
    -------
    int
        Level (100: curtain down; 0: curtain up).
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_curtain_status)
    response_xml = ET.fromstring(response.text)
    bedroom_curtain_status = int(response_xml.text)

    return bedroom_curtain_status

def bedroom_curtain_up():
    """Raises the bedroom curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_curtain_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def bedroom_curtain_down():
    """Rolls down the bedroom curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_bedroom_curtain_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_class_curtain_status():
    """Gets the class curtain status.

    Returns
    -------
    int
        Level (100: curtain down; 0: curtain up).
    """

    response = requests.get(url_spaceLYnk, params=params_class_curtain_status)
    response_xml = ET.fromstring(response.text)
    class_curtain_status = int(response_xml.text)

    return class_curtain_status

def class_curtain_up():
    """Raises the class curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    
    response = requests.get(url_spaceLYnk, params=params_class_curtain_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def class_curtain_down():
    """Rolls down the class curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_class_curtain_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def get_livroom_curtain_status():
    """Gets the living room curtain status.

    Returns
    -------
    int
        Level (100: curtain down; 0: curtain up).
    """

    response = requests.get(url_spaceLYnk, params=params_livroom_curtain_status)
    response_xml = ET.fromstring(response.text)
    livroom_curtain_status = int(response_xml.text)

    return livroom_curtain_status

def livroom_curtain_up():
    """Raises the living room curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """
    
    response = requests.get(url_spaceLYnk, params=params_livroom_curtain_up)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

def livroom_curtain_down():
    """Rolls down the living room curtain.

    Returns
    -------
    bool
        True: Success.
        False: Error.
    """

    response = requests.get(url_spaceLYnk, params=params_livroom_curtain_down)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return True

    return False

# Information from sensors

def get_radiation_level():
    """Gets the outside raditation level.

    Returns
    -------
    float
        Raditation level.
    """

    response = requests.get(url_spaceLYnk, params=params_get_radiation_level)
    response_xml = ET.fromstring(response.text)
    raditaion_level = float(response_xml.text)

    return raditaion_level

def get_rain_status():
    """Determines whether is raining or not.

    Returns
    -------
    bool
        True: It is raining.
        False: It isn"t raining.
    """

    response = requests.get(url_spaceLYnk, params=params_rain_status)
    response_xml = ET.fromstring(response.text)

    if(response_xml.text == "true"):
        return False

    return True

def get_wind_speed():
    """Determines the wind speed.

    Returns
    -------
    float
        Wind speed (m/s).
    """

    response = requests.get(url_spaceLYnk, params=params_wind_speed)
    response_xml = ET.fromstring(response.text)
    wind_speed = float(response_xml.text)

    return wind_speed
