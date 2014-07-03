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
except:
    pass

#print stick.get_numaxes(), stick.get_numballs(), stick.get_numhats(), stick.get_numbuttons()
joystickID = stick.get_numaxes() + stick.get_numballs() + stick.get_numhats() + stick.get_numbuttons()

print "%s" % joystickID
print "%016X" % joystickID

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



;sms, Port 1, Gamepad: Fire 1/Start
sms.input.port1.gamepad.fire1 keyboard 258

;sms, Port 1, Gamepad: Fire 2
sms.input.port1.gamepad.fire2 keyboard 259

;sms, Port 1, Gamepad: Pause
sms.input.port1.gamepad.pause keyboard 13

;sms, Port 1, Gamepad: DOWN
sms.input.port1.gamepad.down keyboard 115

;sms, Port 1, Gamepad: LEFT
sms.input.port1.gamepad.left keyboard 97

;sms, Port 1, Gamepad: RIGHT
sms.input.port1.gamepad.right keyboard 100

;sms, Port 1, Gamepad: UP
sms.input.port1.gamepad.up keyboard 119



    """ % (convert_event(controller_mapping['1'], 100),
    convert_event(controller_mapping['2'], 99),
    convert_event(controller_mapping['PAUSE'], 273),
    convert_event(controller_mapping['DOWN'], 13),
    convert_event(controller_mapping['LEFT'], 9),
    convert_event(controller_mapping['RIGHT'], 276),
    convert_event(controller_mapping['UP'], 274))

except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
