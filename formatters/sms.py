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
def convert_event(event, default):

	if event["type"] in [2,3]:
		foo = "%s %s" % ('keyboard', event["key"])
		return foo
	elif event["type"] in [10,11]:
		foo = "joystick %016X %08x" % (event["joystickID"], event["button"])
		return foo
	elif event["type"] == 7:
		if event["value"] > 0:
			foo = "joystick %016X %08x" % (event["joystickID"], event["axis"] ^ 0x8000)
		elif event["value"] < 0:
			foo = "joystick %016X %08x" % (event["joystickID"], event["axis"] ^ 0xc000)
		return foo
	return default

player1 = (convert_event(controller_mapping[0]['1'], 100),
    convert_event(controller_mapping[0]['2'], 99),
    convert_event(controller_mapping[0]['PAUSE'], 273),
    convert_event(controller_mapping[0]['DOWN'], 13),
    convert_event(controller_mapping[0]['LEFT'], 9),
    convert_event(controller_mapping[0]['RIGHT'], 276),
    convert_event(controller_mapping[0]['UP'], 274),
    convert_event(controller_mapping[0]['*EXIT_PROGRAM'], 2))
	
player2 = ((convert_event(controller_mapping[1]['1'], 100),
    convert_event(controller_mapping[1]['2'], 99),
    convert_event(controller_mapping[1]['PAUSE'], 273),
    convert_event(controller_mapping[1]['DOWN'], 13),
    convert_event(controller_mapping[1]['LEFT'], 9),
    convert_event(controller_mapping[1]['RIGHT'], 276),
    convert_event(controller_mapping[1]['UP'], 274))
	if num_players > 1 else (("",) * 7))
	
	
try:
    output_file_data = """


sms.input.port1 gamepad

;sms, Port 1, Gamepad: Fire 1/Start
sms.input.port1.gamepad.fire1 %s

;sms, Port 1, Gamepad: Fire 2
sms.input.port1.gamepad.fire2 %s

;sms, Port 1, Gamepad: Pause
sms.input.port1.gamepad.pause %s

;sms, Port 1, Gamepad: DOWN
sms.input.port1.gamepad.down %s

;sms, Port 1, Gamepad: LEFT
sms.input.port1.gamepad.left %s

;sms, Port 1, Gamepad: RIGHT
sms.input.port1.gamepad.right %s

;sms, Port 1, Gamepad: UP
sms.input.port1.gamepad.up %s

;Exit
command.exit %s

sms.input.port2 gamepad

;sms, Port 2, Gamepad: Fire 1/Start
sms.input.port2.gamepad.fire1 %s

;sms, Port 2, Gamepad: Fire 2
sms.input.port2.gamepad.fire2 %s

;sms, Port 2, Gamepad: Pause
sms.input.port2.gamepad.pause %s

;sms, Port 2, Gamepad: DOWN
sms.input.port2.gamepad.down %s

;sms, Port 2, Gamepad: LEFT
sms.input.port2.gamepad.left %s

;sms, Port 2, Gamepad: RIGHT
sms.input.port2.gamepad.right %s

;sms, Port 2, Gamepad: UP
sms.input.port2.gamepad.up %s


    """ % ( player1 + player2 )

except KeyError, e:
    print "Your input controller configuration didn't support a required button. Error: %s button required." % str(e)
    sys.exit()

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."
