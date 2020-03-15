import speech_recognition as sr
import os
import json
import time
from gtts import gTTS
# from pydub import AudioSegment
# from pydub.playback import play


def listen(wait_timeout=None):
    # initalize
    r = sr.Recognizer()
    mic = sr.Microphone(1) # decide the microphone based on input to the function

    with mic as source:
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


def wait_for_response_and_respond(note):
    print("listening for a response...")
    response = listen(2)
    print(f"response we found was: {response}")
    if response == "elaborate" or response == "tell me more":
        print("recieved valid response")
        speak_line(note["description"])
        time.sleep(3)
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
        speak_line(note["name"])
        wait_for_response_and_respond(note)


def speak_line(line):
    language = 'en'
    audio_obj = gTTS(text=line, lang=language, slow=False) 
    audio_obj.save("audio.mp3")
    # sound = AudioSegment.from_mp3('audio.mp3')
    # play(sound)
    os.system("open audio.mp3")
    time.sleep(1)
    

speak_main("recipies")

"""
Major Next Steps:
1. Listen in the background: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
2. Dynamic listening to trigger sentence: verb (e.g. cook, order, eat, drink, party) and tags. '... cook ... tags=[italian, soup, ...]'
3. Check how long the 'line' is and estimate how long to wait for the mp3 to play...
    3a. figure out a way for python to know when the song is done. (e.g. simpleaudio)
4. maybe incorperate a database... 
"""


