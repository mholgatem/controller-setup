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
    elif event["type"] == 11:
        return event["button"]
    elif event["type"] == 7:
        return event["axis"]
    else:
        print "Encountered unknown event type %d. Using default." % event["type"]
    return default

output_file_data = """
joy_pad1_up  = joystick0-axis1-min
joy_pad1_down  = joystick0-axis1-max
joy_pad1_left  = joystick0-axis0-min
joy_pad1_right  = joystick0-axis0-max
joy_pad1_a  = joystick0-button%s
joy_pad1_b  = joystick0-button%s
joy_pad1_c  = joystick0-button%s
joy_pad1_x  = joystick0-button%s
joy_pad1_y  = joystick0-button%s
joy_pad1_z  = joystick0-button%s
joy_pad1_mode  = joystick0-button%s
joy_pad1_start  = joystick0-button%s



""" % (convert_event(controller_mapping['A'], 100), 
convert_event(controller_mapping['B'], 99),
convert_event(controller_mapping['C'], 115), 
convert_event(controller_mapping['X'], 120), 
convert_event(controller_mapping['Y'], 97),
convert_event(controller_mapping['Z'], 102), 
convert_event(controller_mapping['START'], 13), 
convert_event(controller_mapping['MODE'], 9))

with open(output_file_name, "w") as output_file:
    output_file.write(output_file_data)

print output_file_name + " created."