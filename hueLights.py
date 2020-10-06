import requests as r
import json

r.packages.urllib3.disable_warnings()

with open('secrets.json') as json_file:
    secrets = json.load(json_file)

LIVING_ROOM = 0
STUDY = 1
ALL = -1
ROOMS = {LIVING_ROOM: [1, 3, 4, 5], STUDY: [2, 6], ALL: [1,2,3,4,5,6]}

HUE_USER_ID = secrets["hue_user"]
HUE_API_BASE = "https://"+secrets["hue_bridge_ip"]+"/api/"+HUE_USER_ID+"/"
HUE_GET_LIGHT = HUE_API_BASE+"lights/{0}/"
HUE_SET_LIGHT = HUE_GET_LIGHT+"state/"

on_setting = {"on":True}
off_setting = {"on":False}

bri_max = {"on":True,"bri":254}
bri_mid = {"on":True,"bri":170}
bri_low = {"on":True,"bri":100}
bri_min = {"on":True,"bri":50}

ct_orange = {"on":True,"ct":454}
ct_white = {"on":True,"ct":153}

brightness_dict = {"max": bri_max, "mid": bri_mid, "low": bri_low, "min": bri_min}
ct_dict = {"white": ct_white, "orange": ct_orange}

def toggleLight(lightId):
    ## turn the light with the id on or off
    setting = off_setting if isLightOn(lightId) else on_setting
    setLight(lightId, setting)

def toggleRoom(room, on):
    for lightId in ROOMS[room]:
        setLight(lightId, on_setting if on else off_setting)

def setRoom(room, setting):
    for lightId in ROOMS[room]:
        setLight(lightId, setting)
    
def nudgeTempRoom(room, isWarmer, fine=False):
    for lightId in ROOMS[room]:
        nudgeTempLight(lightId, isWarmer, fine)

def nudgeTempLight(lightId, isWarmer, fine=False):
    curTemp = currentTempLight(lightId)
    warmer = 10 if fine else 40
    cooler = -warmer
    newTemp = curTemp + warmer if isWarmer else cooler
    setLight(lightId, {"on":True, "ct":tempOrLimit(newTemp) })

def tempOrLimit(temp):
    if temp > 454:
        return 454
    if temp < 153:
        return 153
    return temp
    
def setLight(lightId, setting):
    r.put(HUE_SET_LIGHT.format(lightId), json=setting, verify=False)

def briRoom(room, level):
    setRoom(room, brightness_dict[level])

def tempRoom(room, temp):
    setRoom(room, ct_dict[temp])

def briLight(lightId, level):
    setLight(lightId, brightness_dict[level])

def tempLight(lightId, temp):
    setLight(lightId, ct_dict[temp])

def currentBriLight(lightId):
    return getLightJson(lightId)['state']['bri']

def currentTempLight(lightId):
    return getLightJson(lightId)['state']['ct']

def isLightOn(lightId):
    isOn = getLightJson(lightId)['state']["on"]
    return isOn

def getLightJson(lightId):
    return r.get(HUE_GET_LIGHT.format(lightId), verify=False).json()
