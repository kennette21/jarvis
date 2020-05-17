import speech_recognition as sr
import os
import json
import time
from gtts import gTTS
import playsound as ps
# from pydub import AudioSegment
# from pydub.playback import play


# if a uer says any of these things the program will do the action: elaborate, repeat, or select
ELLABORATE_RESPONSES = ["elaborate", "more", "details", "what is that"]
REPEAT_RESPONSES = ["repeat", "pardon", "that was messed up", "no idea what you said", "what did you say"]
SELECT_RESPONSES = ["select", "i want that one", "give me that"]

ACTIVATE_WORDS = ["Jarvis", "Cortana", "wizard", "bob", "beth"]
RECIPIE_WORDS = ["cook", "recipie", "kitchen"]

r = sr.Recognizer()
mic = sr.Microphone() # decide the microphone based on input to the function

def listen(wait_timeout=None):
    # initalize
    # r1 = sr.Recognizer()
    mic1 = sr.Microphone() # decide the microphone based on input to the function

    with mic1 as source:
        # r.adjust_for_ambient_noise(source) # if noisy
        try:
            audio = r.listen(source, timeout=wait_timeout)
            return r.recognize_google(audio_data=audio) ## extend with all-results param to get other possibles
        except sr.WaitTimeoutError:
            ## continue b/c nothing was said in threshhold time
            return
        except:
            ## something else went wrong, break out
            print("something else went wrong")
            return


def listen_and_analyse_response(note):
    print("listening for a response...")
    response = listen(1)

    # analyse
    if response in ELLABORATE_RESPONSES:
        print("recieved valid response: '{response}'")
        speak_line(note["description"])
    if response in REPEAT_RESPONSES:
        speak_line(note["name"])
        print('repeating but gotta setup recursion, so still moving on')
    if response in SELECT_RESPONSES:
        speak_line("opening browser tab with details")
        return # break
    elif response:
        print("recieved unrecognized response")
        speak_line("unrecognized response, moving on...") ## should ask them to retry
    else:
        print("no response in wait timout, moving on")
        pass


def speak_main(note_type, tags=None):
    print(f"reading json file of {note_type}")
    with open(f'notes/{note_type}.json', 'r') as f:
        note_dict = json.load(f)

    print(f"iteraing over {note_type}s and waiting for a response")
    for note in note_dict:
        if not tags or set(note["tags"]) & set(tags):
            speak_line(note["name"])
            listen_and_analyse_response(note)


def speak_line(line):
    language = 'en'
    audio_obj = gTTS(text=line, lang=language, slow=False) 
    audio_obj.save("audio.mp3")
    ps.playsound('audio.mp3')
    return
        
def parse_activation_phrase(recognizer, audio):
    try:
        audio_string = r.recognize_google(audio)
        word_list = audio_string.split()
        if set(word_list) & set(ACTIVATE_WORDS):
            speak_main("recipies", ["soup"]) # should call note type and tags based on recieved audio
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def handle_passive_listening(recognizer, audio):
    parse_activation_phrase(recognizer, audio)


# speak_main("recipies", ["mexican"])

with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    parse_activation_phrase(audio)
    
# stop_listening = r.listen_in_background(mic, handle_passive_listening) ## this is a problem. We need to start list

# for _ in range(1000): time.sleep(0.1) # run the program for 10 seconds or something and wait for activation phrase

# stop_listening()

"""
Major Next Steps:
1. Listen in the background: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py sort of done
2. Dynamic listening to trigger sentence: verb (e.g. cook, order, eat, drink, party) and tags. '... cook ... tags=[italian, soup, ...]'
4. maybe incorperate a database... 
"""


