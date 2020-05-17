import pvporcupine

handle = pvporcupine.create(keyword_file_paths=['wakewords/jarvis_mac_2020-06-03_v1.7.0.ppn'])

print("sample rate: " + str(handle.sample_rate))
print ("frame length: " + str(handle.frame_length))

## go in a while loop and tell me when you detect the wakework jarvis
try:
    while True:
        # detected = handle.process(get_next_audio_frame())
        detected = False
        if detected:
            print("you said JARVIS!")
except KeyboardInterrupt:
    print("interupted, deleting handler")
    handle.delete()
    pass

def get_next_audio_frame():
    return # some audio frame
