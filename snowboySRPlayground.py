#!/usr/bin/env python3


import pyaudio
import jarvis
import speech_recognition as sr

try:
	r = sr.Recognizer()

	while True:
		mic = sr.Microphone()
		with mic as source:
			print("jarvis is listening")
			audio = r.listen(source, snowboy_configuration=("/Users/thomasbean/projects/deps/snowboy/swig/Python3", ["wakewords/jarvis.pmdl"]))
			word_list = jarvis.collect_word_list(audio)
			if word_list:
				print("found a word list")
				jarvis.parse_command_module(word_list)
finally:
	print("finally closed")
