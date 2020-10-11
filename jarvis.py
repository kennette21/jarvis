import speech_recognition as sr
import os
import json
import time
from gtts import gTTS
import playsound as ps
import hueLights

## words to activate a particular command moduele ##
## lights, food recomendations, take notes, video, audiobooks, etc ##
LIGHT_WORDS = ["lights", "light"]
FOOD_WORDS = ["cook", "recipie", "kitchen"]

## LIGHT commands ##
ON_COMMANDS = ["turn on", "on", "illuminate"]
OFF_COMMANDS = ["off", "darkness"]
BRIGHTEN_COMMANDS = ["brighter", "bright", "more"]
DIM_COMMANDS = ["dimmer", "dim", "less"]

WARMER_COMMANDS = ["warmer"]
COOLER_COMMANDS = ["cooler"]

LIVING_ROOM = ["living room", "living", "room", "main"]
STUDY = ["study"]
ALL = ["all"]

## NOTES WORDS ##
# if a user says any of these things the program will do the action: elaborate, repeat, or select
ELLABORATE_RESPONSES = ["elaborate", "more", "details", "what is that"]
REPEAT_RESPONSES = ["repeat", "pardon", "that was messed up", "no idea what you said", "what did you say"]
SELECT_RESPONSES = ["select", "i want that one", "give me that"]
r = sr.Recognizer()

def start_listening():
    mic = sr.Microphone()

    with mic as source:
        print("jarvis is listening")
        audio = r.listen(source, timeout=2)
        word_list = collect_word_list(audio)
        if word_list:
            print("found a word list")
            parse_command_module(word_list)

def collect_word_list(audio):
    try:
        word_list = r.recognize_google(audio).split()
        print("Google Speech Recognition thinks you said " + str(word_list))
        return(word_list)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return(None)
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return(None)

def parse_command_module(word_list):
    print("parsing command module from: "+ str(word_list))
    if (set(word_list) & set(LIGHT_WORDS)):
        parse_light_command(word_list)
    else:
        print("no light command found, so i stop because i am simple")

def parse_light_command(command_list):
    print("parsing light command from: "+ str(command_list))
    room_id = get_light_location(command_list)
    print("room id: " + str(room_id))
    if (set(command_list) & set(ON_COMMANDS)):
        hueLights.toggleRoom(room_id, True)
    elif(set(command_list) & set(OFF_COMMANDS)):
        hueLights.toggleRoom(room_id, False)
    elif(set(command_list) & set(BRIGHTEN_COMMANDS)):
        ## make the whole dimming thing work better. 
        # pass a nudge command either up or down. need to refactor
        hueLights.briRoom(room_id, "max")
    elif(set(command_list) & set(DIM_COMMANDS)):
        hueLights.briRoom(room_id, "low")
    elif(set(command_list) & set(WARMER_COMMANDS)):
        hueLights.nudgeTempRoom(room_id, True)
        ## have jarvis stop and ask if we want to keep going
    elif(set(command_list) & set(COOLER_COMMANDS)):
        hueLights.nudgeTempRoom(room_id, False)

def get_light_location(command_list):
    if (set(command_list) & set(LIVING_ROOM)):
        return 0
    elif (set(command_list) & set(STUDY)):
        return 1
    elif (set(command_list) & set(ALL)):
        return -1
    else:
        return -1 # default to all
    ## TODO: add individual light functionality

