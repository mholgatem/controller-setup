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
num_players = len(controller_mapping)

# #  Converts our mapping into a emulator specific value
# def convert_event(event, default, joystick):
#     if event["type"] == 3 and not joystick:
#         return pygame.key.name(int(event["key"]))
#     return default

#  Converts our mapping into a emulator specific value
def convert_event(event, default, joystick):

	if event["type"] in [2,3] and not joystick:
		key_name = event["keyname"].replace('left ','l').replace('right ', 'r')
		if key_name != 'unknown key':
			return key_name
	elif event["type"] in [10,11] and joystick:
		#"joystick0-button1"
		joystick_button = "joystick%d-button%d" % (event['joy'], event['button'])
		return joystick_button
	elif event["type"] == 7 and joystick:
		#"joystick0-axis1-min"
		min_max = "min" if event['value'] < 0 else "max"
		joystick_move = "joystick%d-axis%d-%s" % (event['joy'], event['axis'], min_max)
		return joystick_move
	return default
 

player1 = (convert_event(controller_mapping[0]['UP'], 'up', False),
    convert_event(controller_mapping[0]['DOWN'], 'down', False),
    convert_event(controller_mapping[0]['LEFT'], 'left', False),
    convert_event(controller_mapping[0]['RIGHT'], 'right', False),
    convert_event(controller_mapping[0]['A'], 'a', False),
    convert_event(controller_mapping[0]['B'], 's', False),
    convert_event(controller_mapping[0]['C'], 'd', False),
    convert_event(controller_mapping[0]['X'], 'q', False),
    convert_event(controller_mapping[0]['Y'], 'w', False),
    convert_event(controller_mapping[0]['Z'], 'e', False),
    convert_event(controller_mapping[0]['MODE'], 'backspace', False),
    convert_event(controller_mapping[0]['START'], 'return', False),
	convert_event(controller_mapping[0]['*EXIT_PROGRAM'], 'escape', False),
	convert_event(controller_mapping[0]['*RESET'], 'tab', False))
	
player2 = ((convert_event(controller_mapping[1]['UP'], 'kp_up', False),
    convert_event(controller_mapping[1]['DOWN'], 'kp_down', False),
    convert_event(controller_mapping[1]['LEFT'], 'kp_left', False),
    convert_event(controller_mapping[1]['RIGHT'], 'kp_right', False),
    convert_event(controller_mapping[1]['A'], 'delete', False),
    convert_event(controller_mapping[1]['B'], 'end', False),
    convert_event(controller_mapping[1]['C'], 'page_down', False),
    convert_event(controller_mapping[1]['X'], 'insert', False),
    convert_event(controller_mapping[1]['Y'], 'home', False),
    convert_event(controller_mapping[1]['Z'], 'page_up', False),
    convert_event(controller_mapping[1]['MODE'], 'kp_plus', False),
    convert_event(controller_mapping[1]['START'], 'kp_enter', False)) 
	if num_players > 1 else (('',) * 12))
	
joypad1= (convert_event(controller_mapping[0]['UP'], 5, True),
	convert_event(controller_mapping[0]['DOWN'], 5, True),
	convert_event(controller_mapping[0]['LEFT'], 5, True),
	convert_event(controller_mapping[0]['RIGHT'], 5, True),
	convert_event(controller_mapping[0]['A'], 5, True),
    convert_event(controller_mapping[0]['B'], 6, True),
    convert_event(controller_mapping[0]['C'], 9, True),
    convert_event(controller_mapping[0]['X'], 8, True),
    convert_event(controller_mapping[0]['Y'], 0, True), 
    convert_event(controller_mapping[0]['Z'], 0, True), 
    convert_event(controller_mapping[0]['START'], 0, True), 
    convert_event(controller_mapping[0]['MODE'], 1, True))
	
joypad2 = ((convert_event(controller_mapping[1]['UP'], 5, True),
	convert_event(controller_mapping[1]['DOWN'], 5, True),
	convert_event(controller_mapping[1]['LEFT'], 5, True),
	convert_event(controller_mapping[1]['RIGHT'], 5, True),
	convert_event(controller_mapping[1]['A'], 5, True),
    convert_event(controller_mapping[1]['B'], 6, True),
    convert_event(controller_mapping[1]['C'], 9, True),
    convert_event(controller_mapping[1]['X'], 8, True),
    convert_event(controller_mapping[1]['Y'], 0, True), 
    convert_event(controller_mapping[1]['Z'], 0, True), 
    convert_event(controller_mapping[1]['START'], 0, True), 
    convert_event(controller_mapping[1]['MODE'], 1, True)) 
	if num_players > 1 else (('0',)*12))




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

# Quit dgen
key_quit = %s
# Reset Genesis
key_reset = %s

# The same for pad 2
# Yes, I KNOW the default player 2 keys are awful. Pick your own!
key_pad2_up = %s
key_pad2_down = %s
key_pad2_left = %s
key_pad2_right = %s
key_pad2_a = %s
key_pad2_b = %s
key_pad2_c = %s
key_pad2_x = %s
key_pad2_y = %s
key_pad2_z = %s
key_pad2_mode = %s
key_pad2_start = %s

# Fix checksum, needed by some games with Game Genie codes
key_fix_checksum = f1

# Toggle split screen and crap-tv
key_splitscreen_toggle = f4
key_craptv_toggle = f5
# Screenshot
key_screenshot = f12
# Toggle fullscreen mode
key_fullscreen_toggle = alt-enter

# Use this to toggle which CPU core to use, no need to reset!  :)
# If you don't have multiple CPU cores, it won't do anything!
key_cpu_toggle = f11

# This pauses emulation :)
key_stop = z

# Pick save slot
key_slot_0 = f10
key_slot_1 = f1
key_slot_2 = f2
key_slot_3 = f3
key_slot_4 = f4
key_slot_5 = f5
key_slot_6 = f6
key_slot_7 = f7
key_slot_8 = f8
key_slot_9 = f9

# Save/load game to current slot
key_save = f12
key_load = f11

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
int_info_height = -1
int_width = -1
int_height = -1
int_scale = -1
int_scale_x = -1
int_scale_y = -1
int_depth = 0
bool_swab = false
bool_opengl = true
bool_opengl_aspect = true
bool_opengl_linear = true
bool_opengl_32bit = true
bool_opengl_swap = false
bool_opengl_square = false
bool_doublebuffer = true
bool_screen_thread = false

# Use a joystick?
bool_joystick = yes

# Use OpenGL mode?
bool_opengl = no
# Set these to the resolution you want to run OpenGL mode in.
int_opengl_width = -1
int_opengl_height = -1

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
joy_pad1_up = %s
joy_pad1_down = %s
joy_pad1_left = %s
joy_pad1_right = %s
joy_pad1_a = %s
joy_pad1_b = %s
joy_pad1_c = %s
joy_pad1_x = %s
joy_pad1_y = %s
joy_pad1_z = %s
joy_pad1_start = %s
joy_pad1_mode = %s

# Joypad 2
joy_pad2_up = %s
joy_pad2_down = %s
joy_pad2_left = %s
joy_pad2_right = %s
joy_pad2_a = %s
joy_pad2_b = %s
joy_pad2_c = %s
joy_pad2_x = %s
joy_pad2_y = %s
joy_pad2_z = %s
joy_pad2_start = %s
joy_pad2_mode = %s
""" % (player1 + player2 + joypad1 + joypad2)

    


except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

directory = os.path.dirname(output_file_name)
if not os.path.exists(directory):
    os.makedirs(directory)

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
