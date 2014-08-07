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
num_players = len(controller_mapping)

#  Converts our mapping into a emulator specific value
def convert_event(event, default):

	if event["type"] == 3:
		foo = "%s %s" % ('keyboard', event["key"])
		return foo
	elif event["type"] == 11:
		foo = "joystick %016X %08x" % (joystickID, event["button"])
		return foo
	elif event["type"] == 7:
		if event["value"] > 0:
			foo = "joystick %016X %08x" % (joystickID, event["axis"] ^ 0x8000)
		elif event["value"] < 0:
			foo = "joystick %016X %08x" % (joystickID, event["axis"] ^ 0xc000)
		return foo
	return default

player1 = (convert_event(controller_mapping[0]['I'], 100),
    convert_event(controller_mapping[0]['II'], 99),
    convert_event(controller_mapping[0]['RUN'], 273),
    convert_event(controller_mapping[0]['SELECT'], 14),
    convert_event(controller_mapping[0]['DOWN'], 13),
    convert_event(controller_mapping[0]['LEFT'], 9),
    convert_event(controller_mapping[0]['RIGHT'], 276),
    convert_event(controller_mapping[0]['UP'], 274),
    convert_event(controller_mapping[0]['*EXIT_PROGRAM'], 2))
	
player2 = ((convert_event(controller_mapping[1]['I'], 100),
    convert_event(controller_mapping[1]['II'], 99),
    convert_event(controller_mapping[1]['RUN'], 273),
    convert_event(controller_mapping[1]['SELECT'], 14),
    convert_event(controller_mapping[1]['DOWN'], 13),
    convert_event(controller_mapping[1]['LEFT'], 9),
    convert_event(controller_mapping[1]['RIGHT'], 276),
    convert_event(controller_mapping[1]['UP'], 274)) 
	if num_players > 1 else (("",) * 8))

try:
    output_file_data = """

pce_fast.input.port1 gamepad

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

pce_fast.input.port2 gamepad

;pce_fast, Port 2, Gamepad: I
pce_fast.input.port2.gamepad.i %s

;pce_fast, Port 2, Gamepad: II
pce_fast.input.port2.gamepad.ii %s

;pce_fast, Port 2, Gamepad: RUN
pce_fast.input.port2.gamepad.run %s

;pce_fast, Port 2, Gamepad: SELECT
pce_fast.input.port2.gamepad.select %s

;pce_fast, Port 2, Gamepad: DOWN
pce_fast.input.port2.gamepad.down %s  

;pce_fast, Port 2, Gamepad: LEFT
pce_fast.input.port2.gamepad.left %s

;pce_fast, Port 2, Gamepad: RIGHT
pce_fast.input.port2.gamepad.right %s

;pce_fast, Port 2, Gamepad: UP
pce_fast.input.port2.gamepad.up %s


    """ % ( player1 + player2 )

except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
