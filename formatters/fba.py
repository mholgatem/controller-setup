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
def convert_event(event, default, joystick=False):
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

    #player 2 keyboard controls, disabled by default
    A_2=999
    B_2=999
    X_2=999
    Y_2=999
    L_2=999
    R_2=999
    START_2=999
    SELECT_2=999
    LEFT_2=999
    RIGHT_2=999
    UP_2=999
    DOWN_2=999

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
    #Joystick axis
    JA_LR=%d
    JA_UD=%d
    #player 2 button configuration
    A_2=0
    B_2=1
    X_2=2
    Y_2=3
    L_2=4
    R_2=6
    START_2=9
    SELECT_2=8
    #Joystick axis
    JA_LR_2=0
    JA_UD_2=1

    [Graphics]
    DisplaySmoothStretch=1
    # Display Effect: 0 none, 1 scanlines
    DisplayEffect=0
    DisplayBorder=0
    MaintainAspectRatio=1

    [Sound]


    """ % (convert_event(controller_mapping['Top 1'], 100, False), 
        convert_event(controller_mapping['Top 2'], 99, False),
     convert_event(controller_mapping['Top 3'], 115, False), 
     convert_event(controller_mapping['Bottom 1'], 120, False), 
     convert_event(controller_mapping['Bottom 2'], 97, False),
     convert_event(controller_mapping['Bottom 3'], 102, False), 
     convert_event(controller_mapping['START'], 13, False), 
     convert_event(controller_mapping['COIN'], 9, False),
     convert_event(controller_mapping['LEFT'], 276, False), 
     convert_event(controller_mapping['RIGHT'], 275, False), 
     convert_event(controller_mapping['UP'], 273, False),
     convert_event(controller_mapping['DOWN'], 274, False),
      #Now for joystick events
     convert_event(controller_mapping['Top 1'], 3, True), 
     convert_event(controller_mapping['Top 2'], 2, True),
     convert_event(controller_mapping['Top 3'], 1, True), 
     convert_event(controller_mapping['Bottom 1'], 0, True), 
     convert_event(controller_mapping['Bottom 2'], 4, True),
     convert_event(controller_mapping['Bottom 3'], 6, True), 
     convert_event(controller_mapping['START'], 9, True), 
     convert_event(controller_mapping['COIN'], 8, True), 
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