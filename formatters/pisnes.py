import json
import sys
#  TODO Abstract this into a base formatter class
if len(sys.argv) < 3:
    print "Formatter requires 2 arguments, input file and output file name"

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file_data = open(input_file_name).read()
controller_mapping = json.loads(input_file_data)
num_players = len(controller_mapping)

#  Converts our mapping into a emulator specific value
def convert_event(event, default, joystick):

	if event["type"] in [2,3] and not joystick:
		return event["key"]
	elif event["type"] in [10,11] and joystick:
		return event["button"]
	elif event["type"] == 7 and joystick:
		return event["axis"]
	return default
	

player1 = (convert_event(controller_mapping[0]['A'], 100, False), 
     convert_event(controller_mapping[0]['B'], 99, False),
     convert_event(controller_mapping[0]['X'], 115, False), 
     convert_event(controller_mapping[0]['Y'], 120, False), 
     convert_event(controller_mapping[0]['LEFT BUMPER'], 97, False),
     convert_event(controller_mapping[0]['RIGHT BUMPER'], 102, False), 
     convert_event(controller_mapping[0]['START'], 13, False), 
     convert_event(controller_mapping[0]['SELECT'], 9, False),
     convert_event(controller_mapping[0]['LEFT'], 276, False), 
     convert_event(controller_mapping[0]['RIGHT'], 275, False), 
     convert_event(controller_mapping[0]['UP'], 273, False),
     convert_event(controller_mapping[0]['DOWN'], 274, False),
     convert_event(controller_mapping[0]['*EXIT_PROGRAM'], 27, False))
	 
	 
player2 = ((convert_event(controller_mapping[1]['A'], 100, False), 
     convert_event(controller_mapping[1]['B'], 99, False),
     convert_event(controller_mapping[1]['X'], 115, False), 
     convert_event(controller_mapping[1]['Y'], 120, False), 
     convert_event(controller_mapping[1]['LEFT BUMPER'], 97, False),
     convert_event(controller_mapping[1]['RIGHT BUMPER'], 102, False), 
     convert_event(controller_mapping[1]['START'], 13, False), 
     convert_event(controller_mapping[1]['SELECT'], 9, False),
     convert_event(controller_mapping[1]['LEFT'], 276, False), 
     convert_event(controller_mapping[1]['RIGHT'], 275, False), 
     convert_event(controller_mapping[1]['UP'], 273, False),
     convert_event(controller_mapping[1]['DOWN'], 274, False))
	 if num_players > 1 else ((999,) * 12))
	 
	 
	 
      #Now for joystick events
joypad1 = (convert_event(controller_mapping[0]['A'], 3, True), 
     convert_event(controller_mapping[0]['B'], 2, True),
     convert_event(controller_mapping[0]['X'], 1, True), 
     convert_event(controller_mapping[0]['Y'], 0, True), 
     convert_event(controller_mapping[0]['LEFT BUMPER'], 4, True),
     convert_event(controller_mapping[0]['RIGHT BUMPER'], 6, True), 
     convert_event(controller_mapping[0]['START'], 9, True), 
     convert_event(controller_mapping[0]['SELECT'], 8, True), 
     convert_event(controller_mapping[0]['LEFT'], 0, True), 
     convert_event(controller_mapping[0]['UP'], 1, True))
	 
joypad2 = ((convert_event(controller_mapping[1]['A'], 0, True), 
     convert_event(controller_mapping[1]['B'], 1, True),
     convert_event(controller_mapping[1]['X'], 2, True), 
     convert_event(controller_mapping[1]['Y'], 3, True), 
     convert_event(controller_mapping[1]['LEFT BUMPER'], 4, True),
     convert_event(controller_mapping[1]['RIGHT BUMPER'], 6, True), 
     convert_event(controller_mapping[1]['START'], 9, True), 
     convert_event(controller_mapping[1]['SELECT'], 8, True), 
     convert_event(controller_mapping[1]['LEFT'], 0, True), 
     convert_event(controller_mapping[1]['UP'], 1, True)) 
	 if num_players > 1 else (0,1,2,3,4,6,9,8,0,1))
	 
joypad_options = (convert_event(controller_mapping[1]['*EXIT_PROGRAM'], 0, True),)

try:
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
QUIT=%d
ACCEL=999

#player 2 keyboard controls
A_2=%d
B_2=%d
X_2=%d
Y_2=%d
L_2=%d
R_2=%d
START_2=%d
SELECT_2=%d
LEFT_2=%d
RIGHT_2=%d
UP_2=%d
DOWN_2=%d


[Joystick]
# Get codes from "jstest /dev/input/js0"
# from package "joystick"
#player 1 joystick controls
A_1=%d
B_1=%d
X_1=%d
Y_1=%d
L_1=%d
R_1=%d
START_1=%d
SELECT_1=%d
#Joystick axis
JA_LR_1=%d
JA_UD_1=%d

#player 2 joystick controls
A_2=%d
B_2=%d
X_2=%d
Y_2=%d
L_2=%d
R_2=%d
START_2=%d
SELECT_2=%d
#Joystick axis
JA_LR_2=%d
JA_UD_2=%d

#joystick options
QUIT=%d
ACCEL=999
QLOAD=10
QSAVE=11

#XinMo (0=False, 1=True)
XinMoEnabled=0

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
    """ % ( player1 + player2 + joypad1 + joypad2 + joypad_options)
except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."