# What is this?
My playground for all things voice assistant. Some of it works, some not.

# What works now?
hueLights.py is a pretty simple client smacked together to control Philip's lights. It works with the secrets file but still fairly messy.

wakeWordStarter.py is using porcupine wake word detection before actively listening to the next phrase and using SpeechRecognition via google to do speech to text and then act.

wakeOnJarvis.py has succesful wake word detection from mac, but will not work on Pi. It is using Pythons SpeechRecognition library with a snowboy configuration.

jarvis.py is the decision matrix file. The `parse_command_module` method takes an array of words which is the users spoken phrase. It checks the array for keywords which determine if there is a command, and acts accordingly. It is only setup for light control now, but I would like to extend it. Cooking and Recipies, places to go out and eat, places to go.

# Main things to do.
clean up Philips Hue helper as it is one of the only truely useful things for someone outside :d
