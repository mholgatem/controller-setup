import json
import sys
#  TODO Abstract this into a base formatter class
if len(sys.argv) < 3:
    print "Formatter requires 2 arguments, input file and output file name"

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file_data = open(input_file_name).read()
controller_mapping = json.loads(input_file_data)

#  Converts our mapping into a emulator specific value
def convert_event(event):
    if event["type"] == 3:
        return event["key"]
    else:
        print "Encountered unknown event type %d, rerun controller configuration." % event.type

output_file_data = """
[Keyboard]
# Get codes from /usr/include/SDL/SDL_keysym.h
A_1=%d
B_1=%d
X_1=%d
Y_1=%d
L_1=%d
R_1=%d
START_1=%d
SELECT_1=%d
LEFT_1=%d
RIGHT_1=%d
UP_1=%d
DOWN_1=%d
QUIT=27
ACCEL=8

[Joystick]
# Get codes from "jstest /dev/input/js0"
# from package "joystick"
A_1=3
B_1=2
X_1=1
Y_1=0
L_1=4
R_1=6
START_1=9
SELECT_1=8
QUIT=99
ACCEL=7
QLOAD=10
QSAVE=11
#Joystick axis
JA_LR=0
JA_UD=1

[Graphics]
DisplaySmoothStretch=1
# Display Effect: 0 none, 1 scanlines, 2 phospher
# NOTE Phospher does not run at full speed
DisplayEffect=0
MaintainAspectRatio=1
DisplayBorder=0
AutoFrameskip=1
Frameskip=200
Transparency=1
CPUCycles=100

[Sound]
APUEnabled=1
# Sound rates below as index, i.e. 7=44100 (some of these produce static)
# 0, 8192, 11025, 16000, 22050, 29300, 32000, 44100
SoundPlaybackRate=7
InterpolatedSound=0
""" % (convert_event(controller_mapping['A']), convert_event(controller_mapping['B']),
 convert_event(controller_mapping['X']), convert_event(controller_mapping['Y']), convert_event(controller_mapping['Left Bumper']),
 convert_event(controller_mapping['Right Bumper']), convert_event(controller_mapping['START']), convert_event(controller_mapping['SELECT']),
 convert_event(controller_mapping['LEFT']), convert_event(controller_mapping['RIGHT']), convert_event(controller_mapping['UP']),
 convert_event(controller_mapping['DOWN']), )

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."