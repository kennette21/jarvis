import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import hueLights

with open('secrets.json') as json_file:
    secrets = json.load(json_file)

authenticator = IAMAuthenticator(secrets["watson-stt-api-key"])
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(secrets["watson-stt-url"])
study_on_keywords = ['study lights on']

with open('/home/pi/proj/jarvis/test.wav',
               'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        word_alternatives_threshold=0.9,
        keywords=study_on_keywords,
        keywords_threshold=0.5
    ).get_result()
print(json.dumps(speech_recognition_results, indent=2))
result_keywords = speech_recognition_results["results"][0]["keywords_result"]
if result_keywords:
    hueLights.toggleRoom(1, True)
