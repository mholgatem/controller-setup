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
def convert_event(event, default, joystick=False):
    if event["type"] == 3 and not joystick:
            return event["key"]
    else:
        print "Encountered unknown event type %d. Using default." % event.type
    return default

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
QUIT=99
ACCEL=7
QLOAD=10
QSAVE=11
#Joystick axis
JA_LR=%d
JA_UD=%d

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
""" % (convert_event(controller_mapping['A'], 100), convert_event(controller_mapping['B'], 99),
 convert_event(controller_mapping['X'], 115), convert_event(controller_mapping['Y'], 120), convert_event(controller_mapping['Left Bumper'], 97),
 convert_event(controller_mapping['Right Bumper'], 102), convert_event(controller_mapping['START'], 13), convert_event(controller_mapping['SELECT'], 9),
 convert_event(controller_mapping['LEFT'], 276), convert_event(controller_mapping['RIGHT'], 275), convert_event(controller_mapping['UP'], 273),
 convert_event(controller_mapping['DOWN'], 274), #Now for joystick events
 convert_event(controller_mapping['A'], 3, True), convert_event(controller_mapping['B'], 2, True),
 convert_event(controller_mapping['X'], 1, True), convert_event(controller_mapping['Y'], 0, True), convert_event(controller_mapping['Left Bumper'], 4, True),
 convert_event(controller_mapping['Right Bumper'], 6, True), convert_event(controller_mapping['START'], 9, True), convert_event(controller_mapping['SELECT'], 8, True),
 convert_event(controller_mapping['LEFT'], 276, True), convert_event(controller_mapping['RIGHT'], 275, True), convert_event(controller_mapping['UP'], 273, True),
 convert_event(controller_mapping['DOWN'], 274, True))

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."