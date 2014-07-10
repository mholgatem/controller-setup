import json
import sys
import pygame
from pygame.locals import *
import subprocess

pygame.init()
pygame.font.init()
pygame.joystick.init()

try:
    stick = pygame.joystick.Joystick(0)
    stick.init()
    #print stick.get_numaxes(), stick.get_numballs(), stick.get_numhats(), stick.get_numbuttons()
    joystickID = stick.get_numaxes() + stick.get_numballs() + stick.get_numhats() + stick.get_numbuttons()

    print "%s" % joystickID
    print "%016X" % joystickID
except:
    joystickID = 0


#  TODO Abstract this into a base formatter class
if len(sys.argv) < 3:
    print "Formatter requires 2 arguments, input file and output file name"

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

input_file_data = open(input_file_name).read()
controller_mapping = json.loads(input_file_data)

#  Converts our mapping into a emulator specific value
def convert_event(event, default):
    '''
        event = event data
        default = value to default to if joystick doesn't match
        joystick = True if looking for a joystick value
    '''
    if event["type"] == 3:
	foo = "%s %s" % ('keyboard', event["key"])
	#print foo
	return foo
    elif event["type"] == 11:
        foo = "joystick %016X %08x" % (joystickID, event["button"])
    	#print foo
	return foo
    elif event["type"] == 7:
        if event["value"] > 0:
		foo = "joystick %016X %08x" % (joystickID, event["axis"] ^ 0x8000)
	elif event["value"] < 0:
		foo = "joystick %016X %08x" % (joystickID, event["axis"] ^ 0xc000)

	#print event
	#print foo
	return foo
    return default


try:
    output_file_data = """

;pce_fast, Port 1, Gamepad: I
pce_fast.input.port1.gamepad.i %s

;pce_fast, Port 1, Gamepad: II
pce_fast.input.port1.gamepad.ii %s

;pce_fast, Port 1, Gamepad: RUN
pce_fast.input.port1.gamepad.run %s

;pce_fast, Port 1, Gamepad: SELECT
pce_fast.input.port1.gamepad.select %s

;pce_fast, Port 1, Gamepad: DOWN
pce_fast.input.port1.gamepad.down %s  

;pce_fast, Port 1, Gamepad: LEFT
pce_fast.input.port1.gamepad.left %s

;pce_fast, Port 1, Gamepad: RIGHT
pce_fast.input.port1.gamepad.right %s

;pce_fast, Port 1, Gamepad: UP
pce_fast.input.port1.gamepad.up %s

;Exit
command.exit %s


    """ % (convert_event(controller_mapping['I'], 100),
    convert_event(controller_mapping['II'], 99),
    convert_event(controller_mapping['RUN'], 273),
    convert_event(controller_mapping['SELECT'], 14),
    convert_event(controller_mapping['DOWN'], 13),
    convert_event(controller_mapping['LEFT'], 9),
    convert_event(controller_mapping['RIGHT'], 276),
    convert_event(controller_mapping['UP'], 274),
    convert_event(controller_mapping['EXIT_PROGRAM'], 2)

    )

except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
