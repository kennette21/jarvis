#!/usr/bin/env python3

import struct
import pyaudio
import pvporcupine
import jarvis
import speech_recognition as sr

porcupine = None
pa = None
audio_stream = None

try:
	porcupine = pvporcupine.create(keywords=["blueberry"])
	pa = pyaudio.PyAudio()
	audio_stream = pa.open(
					rate=porcupine.sample_rate,
					channels=1,
					format=pyaudio.paInt16,
					input=True,
					frames_per_buffer=porcupine.frame_length)
	r = sr.Recognizer()

	while True:
		print("in the while")
		pcm = audio_stream.read(porcupine.frame_length)
		pcm1 = struct.unpack_from("h" * porcupine.frame_length, pcm)

		keyword_index = porcupine.process(pcm1)

		if keyword_index:
			print("keyword detected, starting to listen with jarvis")
			# jarvis.start_listening()
			## these next  4 lines are a bad hack.
			# TODO: feed the audio into r.listen() from the already existing audio_stream
			if audio_stream is not None:
				audio_stream.close()
			if pa is not None:
				pa.terminate()
			mic = sr.Microphone() 
			with mic as source:
				print("jarvis is listening")
				audio = r.listen(source, timeout=2)
				word_list = jarvis.collect_word_list(audio)
				if word_list:
					print("found a word list")
					jarvis.parse_command_module(word_list)
finally:
	if porcupine is not None:
		porcupine.delete()
	if audio_stream is not None:
		audio_stream.close()
	if pa is not None:
		pa.terminate()
