import json
import sys
import os
#  TODO Abstract this into a base formatter class
if len(sys.argv) < 3:
    print "Formatter requires 2 arguments, input file and output file name"

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file_data = open(input_file_name).read()
controller_mapping = json.loads(input_file_data)

#  Converts our mapping into a emulator specific value
def convert_event(event, default, joystick):
    '''
        event = event data
        default = value to default to if joystick doesn't match
        joystick = True if looking for a joystick value
    '''
    if event["type"] == 3 and not joystick:
            return event["key"]
    elif event["type"] == 11 and joystick:
        return event["button"]
    elif event["type"] == 7 and joystick:
        return event["axis"]
    return default
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
    """ % (convert_event(controller_mapping['A'], 100, False),
    convert_event(controller_mapping['B'], 99, False),
    convert_event(controller_mapping['X'], 115, False),
    convert_event(controller_mapping['Y'], 120, False),
    convert_event(controller_mapping['Left Bumper'], 97, False),
    convert_event(controller_mapping['Right Bumper'], 102, False),
    convert_event(controller_mapping['START'], 13, False),
    convert_event(controller_mapping['SELECT'], 9, False),
    convert_event(controller_mapping['LEFT'], 276, False),
    convert_event(controller_mapping['RIGHT'], 275, False),
    convert_event(controller_mapping['UP'], 273, False),
    convert_event(controller_mapping['DOWN'], 274, False),
    #Now for joystick events
    convert_event(controller_mapping['A'], 3, True),
    convert_event(controller_mapping['B'], 2, True),
    convert_event(controller_mapping['X'], 1, True),
    convert_event(controller_mapping['Y'], 0, True),
    convert_event(controller_mapping['Left Bumper'], 4, True),
    convert_event(controller_mapping['Right Bumper'], 6, True),
    convert_event(controller_mapping['START'], 9, True),
    convert_event(controller_mapping['SELECT'], 8, True),
     convert_event(controller_mapping['LEFT'], 0, True), 
     convert_event(controller_mapping['UP'], 1, True) )
except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

directory = os.path.dirname(output_file_name)
if not os.path.exists(directory):
    os.makedirs(directory)

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."