import json
import sys
import pygame
import os

#  TODO Abstract this into a base formatter class
if len(sys.argv) < 3:
    print "Formatter requires 2 arguments, input file and output file name"

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file_data = open(input_file_name).read()
controller_mapping = json.loads(input_file_data)

# #  Converts our mapping into a emulator specific value
# def convert_event(event, default, joystick):
#     if event["type"] == 3 and not joystick:
#         return pygame.key.name(int(event["key"]))
#     return default

#  Converts our mapping into a emulator specific value
def convert_event(event, default, joystick):
    '''
        event = event data
        default = value to default to if joystick doesn't match
        joystick = True if looking for a joystick value
    '''
    if event["type"] == 3 and not joystick:
        return pygame.key.name(int(event["key"]))
    elif event["type"] == 11 and joystick:
        return event["button"]
    elif event["type"] == 7 and joystick:
        #return "joystick%s-axis%s-min" % (event["axis"], 
	return default

#  Dgen does things backwards... so we convert all joystick input into backwards way here
joystick_lines = ["joypad1_b%d = %s" % (event["button"], identifer) for identifer, event in controller_mapping.iteritems() if event["type"]==11] 

#  we need this to get the text name of keys...
pygame.init()

try:
    output_file_data = """
# Fields beginning with "key_" take key names. The valid key names are listed
# in the dgenrc(5) manpage.

# Fields beginning with "bool_" are boolean, i.e. they take a true or false
# value:
#  "true", "yes", any number except 0: true 
#  "false", "no", "0"                : false

# Fields beginning with "int_" take a _positive_ integer. Simple enough, huh? ;)

# The syntax and fields of this file are documented in a bit more detail in the
# dgenrc(5) manpage.

# These are the controls for pad 1
key_pad1_up = %s
key_pad1_down = %s
key_pad1_left = %s
key_pad1_right = %s
key_pad1_a = %s
key_pad1_b = %s
key_pad1_c = %s
key_pad1_x = %s
key_pad1_y = %s
key_pad1_z = %s
key_pad1_mode = %s
key_pad1_start = %s

# The same for pad 2
# Yes, I KNOW the default player 2 keys are awful. Pick your own!
key_pad2_up = kp_up
key_pad2_down = kp_down
key_pad2_left = kp_left
key_pad2_right = kp_right
key_pad2_a = delete
key_pad2_b = end
key_pad2_c = page_down
key_pad2_x = insert
key_pad2_y = home
key_pad2_z = page_up
key_pad2_mode = kp_plus
key_pad2_start = kp_enter

# Fix checksum, needed by some games with Game Genie codes
key_fix_checksum = f1

# Quit dgen
key_quit = escape
# Toggle split screen and crap-tv
key_splitscreen_toggle = f4
key_craptv_toggle = f5
# Screenshot
key_screenshot = f12
# Reset Genesis
key_reset = tab
# Toggle fullscreen mode
key_fullscreen_toggle = alt-enter

# Use this to toggle which CPU core to use, no need to reset!  :)
# If you don't have multiple CPU cores, it won't do anything!
key_cpu_toggle = f11

# This pauses emulation :)
key_stop = z

# Pick save slot
key_slot_0 = 0
key_slot_1 = 1
key_slot_2 = 2
key_slot_3 = 3
key_slot_4 = 4
key_slot_5 = 5
key_slot_6 = 6
key_slot_7 = 7
key_slot_8 = 8
key_slot_9 = 9
# Save/load game to current slot
key_save = f2
key_load = f3

# This sets whether split-screen and crap-tv should be enabled on startup.
bool_splitscreen_startup = no
# There are now multiple CTV effects to try. Pick your favorite:
#  off       - No CTV
#  blur      - Blur bitmap (this is the CTV from older versions)
#  scanline  - Attenuate every other scanline, by Phillip K. Hornung <redx@pknet.com>
#  interlace - Unstable crappy television (I had one that looked like this ;), by me!
ctv_craptv_startup = off

# These decide whether DGen should automatically load slot 0 on startup,
# and/or autosave to slot 0 on exit.
bool_autoload = no
bool_autosave = no

# Skip frames to keep time? (faster, but can make things look bad)
# This doesn't matter if you have sound enabled, since the sound code has its
# own frameskipping
bool_frameskip = yes
# Show cartridge header info at startup, like Snes9X? Causes a 3-second pause,
# but might be interesting to hackers or other curious people (like me :)
bool_show_carthead = no

# Sound?
bool_sound = yes
# The sound rate to use.
int_soundrate = 22050
# Leave this true for 16-bit sound, but if you're unfortunate enough to have
# an old 8-bit card make it false.
bool_16bit = yes
# Number of sound segments for buffering.  Lower values yield faster
# speed, and less latency in controls and sound, but at the cost of CPU
# Values can be 4, 8, 16, or 32 (frames)
int_soundsegs = 8

# This is how many microseconds DGen should sleep every frame. Even little
# amounts can decrease CPU overhead significantly, and the default of 20
# doesn't hurt performance terribly. Of course, set it to 0 if you don't
# mind DGen eating all your CPU (like me ;)
int_nice = 0

# Run fullscreen?
bool_fullscreen = no

# If you want to increase the size of the window, increase this value.
# It currently must be a whole number.
int_scale = 1

# Use a joystick?
bool_joystick = yes

# Use OpenGL mode?
bool_opengl = no
# Set these to the resolution you want to run OpenGL mode in.
int_opengl_width = 640
int_opengl_height = 480

# These are the joypad mappings for both controllers.  Defaults are
# tailored for Gravis GamePad Pros. (10 button)  Configure the variables:
# joypadX_bY, where X is the joypad number (1 or 2) and Y is the
# corresponding button.  It may take some tweaking to get the values just
# right.  You can define up to 16 buttons (0-15) and can define Genesis
# buttons more than once and can leave them blank.  Acceptable identifiers
# are:
# A, a, B, b, C, c, X, x, Y, y, Z, z, MODE, mode, M, m, START, start, S, s

# NOTE:  For now, you have to uncomment the buttons you are using, or the
# default mappings will be used.  You will get warnings about invalid RC
# lines if you don't compile joystick support in. [PKH]

# Joypad 1
#joy_pad1_up = 0
#joy_pad1_down = 0
#joy_pad1_left = 0
#joy_pad1_right = 0
joy_pad1_a = %s
joy_pad1_b = %s
joy_pad1_c = %s
joy_pad1_x = %s
joy_pad1_y = %s
joy_pad1_z = %s
joy_pad1_start = %s
joy_pad1_mode = %s

# Joypad 2
#joypad2_b0 = A
#joypad2_b1 = C
#joypad2_b2 = A
#joypad2_b3 = B
#joypad2_b4 = Y
#joypad2_b5 = Z
#joypad2_b6 = X
#joypad2_b7 = X
#joypad2_b8 = START
#joypad2_b9 = MODE
#joypad2_b10 =
#joypad2_b11 =
#joypad2_b12 = 
#joypad2_b13 = 
#joypad2_b14 = 
#joypad2_b15 = 
""" %(convert_event(controller_mapping['UP'], 'up', False),
    convert_event(controller_mapping['DOWN'], 'down', False),
    convert_event(controller_mapping['LEFT'], 'left', False),
    convert_event(controller_mapping['RIGHT'], 'right', False),
    convert_event(controller_mapping['A'], 'a', False),
    convert_event(controller_mapping['B'], 's', False),
    convert_event(controller_mapping['C'], 'd', False),
    convert_event(controller_mapping['X'], 'q', False),
    convert_event(controller_mapping['Y'], 'w', False),
    convert_event(controller_mapping['Z'], 'e', False),
    convert_event(controller_mapping['MODE'], 'backspace', False),
    convert_event(controller_mapping['START'], 'return', False),
    #Now for joystick events
    # convert_event(controller_mapping['UP'], 3, True),
    # convert_event(controller_mapping['DOWN'], 2, True),
    # convert_event(controller_mapping['LEFT'], 1, True),
    # convert_event(controller_mapping['RIGHT'], 4, True),
    convert_event(controller_mapping['A'], 5, True),
    convert_event(controller_mapping['B'], 6, True),
    convert_event(controller_mapping['C'], 9, True),
    convert_event(controller_mapping['X'], 8, True),
    convert_event(controller_mapping['Y'], 0, True), 
    convert_event(controller_mapping['Z'], 0, True), 
    convert_event(controller_mapping['START'], 0, True), 
    convert_event(controller_mapping['MODE'], 1, True) 

    )

    


except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

directory = os.path.dirname(output_file_name)
if not os.path.exists(directory):
    os.makedirs(directory)

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
