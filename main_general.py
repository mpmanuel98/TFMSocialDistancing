"""
Script main_general.py.

This script controls automatically the illumination of the smart home.
If a person enters in a room and the cameras detect movement, the room
is illuminated and a timer starts. If the timer finish and nobody has
been detected, the illumination turns off. In the other hand if someone
is detected, the timer refreshs and continues trying to detect someone.

Also a function is defined:
    wait_for_detection(wait_time)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import time

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.spacelynk_server as SPL

"""
Script
----------
"""

if(args.room_to_control == "bedroom"):
    while True:
        room_motion_alarm = FWC.get_motion_detection_alarm(FWC.url_bedroom)
        print(room_motion_alarm)
        if(room_motion_alarm == 2):
            if(SPL.get_rain_status() == True):
                if(SPL.get_bedroom_lights_status() == False):
                    SPL.bedroom_lights_on()
                    wait_for_detection(300, FWC.url_bedroom)
            else:
                print(SPL.get_radiation_level())
                if(SPL.get_radiation_level() < 1700):
                    if(SPL.get_bedroom_lights_status() == False):
                        SPL.bedroom_lights_on()
                        wait_for_detection(300, FWC.url_bedroom)
                else:
                    if(SPL.get_bedroom_blind_status() > 75):
                        SPL.bedroom_blind_up()
                        wait_for_detection(300, FWC.url_bedroom)
        else:
            if(SPL.get_bedroom_lights_status() == True):
                SPL.bedroom_lights_off()
                time.sleep(5)
            if(SPL.get_bedroom_blind_status() < 25):
                SPL.bedroom_blind_down()
                time.sleep(10)

elif(args.room_to_control == "kitchen"):
    while True:
        room_motion_alarm = FWC.get_motion_detection_alarm(FWC.url_kitchen)
        print(room_motion_alarm)
        if(room_motion_alarm == 2):
            if(SPL.get_rain_status() == True):
                if(SPL.get_kitchen_lights_status() == False):
                    SPL.kitchen_lights_on()
                    wait_for_detection(300, FWC.url_kitchen)
            else:
                print(SPL.get_radiation_level())
                if(SPL.get_radiation_level() < 1700):
                    if(SPL.get_kitchen_lights_status() == False):
                        SPL.kitchen_lights_on()
                        wait_for_detection(300, FWC.url_kitchen)
                else:
                    if(SPL.get_kitchen_blind_status() > 75):
                        SPL.kitchen_blind_up()
                        wait_for_detection(300, FWC.url_kitchen)
        else:
            if(SPL.get_kitchen_lights_status() == True):
                SPL.kitchen_lights_off()
                time.sleep(5)
            if(SPL.get_kitchen_blind_status() < 25):
                SPL.kitchen_blind_down()
                time.sleep(10)
elif(args.room_to_control == "livroom"):
    while True:
        room_motion_alarm = FWC.get_motion_detection_alarm(FWC.url_living_room)
        print(room_motion_alarm)
        if(room_motion_alarm == 2):
            if(SPL.get_rain_status() == True):
                if(SPL.get_livroom_lights_status() == False):
                    SPL.livroom_lights_on()
                    wait_for_detection(300, FWC.url_livroom)
            else:
                print(SPL.get_radiation_level())
                if(SPL.get_radiation_level() < 1700):
                    if(SPL.get_livroom_lights_status() == False):
                        SPL.livroom_lights_on()
                        wait_for_detection(300, FWC.url_living_room)
                else:
                    if(SPL.get_livroom_curtain_status() > 75):
                        SPL.livroom_curtain_up()
                        wait_for_detection(300, FWC.url_living_room)
        else:
            if(SPL.get_livroom_lights_status() == True):
                SPL.livroom_lights_off()
                time.sleep(5)
            if(SPL.get_livroom_curtain_status() < 25):
                SPL.livroom_curtain_down()
                time.sleep(10)
else:
    exit()