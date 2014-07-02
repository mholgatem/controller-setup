import json
import sys
import os
import pygame
from pygame.locals import *
import subprocess


pygame.init()
pygame.font.init()
pygame.joystick.init()

DIRECTORY = "/home/pi/pimame/controller-setup/"

#  Try to initialize the first joystick
try:
    stick = pygame.joystick.Joystick(0)
    stick.init()
except:
    pass

#  Formatters available 
formatters_available = filter(lambda x: x[-3:]==".py", os.listdir(DIRECTORY + 'formatters'))

#  What controller are we configuring?
controllers_available = os.listdir(DIRECTORY +'controllers')

if len(sys.argv) > 1:
    controllers = sys.argv[1:]
else:
    controllers = controllers_available

events_to_capture = [KEYUP, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION]

#  Initialize screen
pygame.display.init()
dinfo = pygame.display.Info()
fullscreen = False

flag = 0
if fullscreen:
    flag = pygame.FULLSCREEN

if (pygame.display.mode_ok((dinfo.current_w,dinfo.current_h),pygame.FULLSCREEN)):
    windowSurface = pygame.display.set_mode((dinfo.current_w, dinfo.current_h), flag)
else:
    pygame.quit()
    sys.exit()



#windowSurface = pygame.display.set_mode((0,0), 0, 32)
window_rect = windowSurface.get_rect()
center_x = window_rect.centerx
center_y = window_rect.centery
window_width = window_rect.width
window_height = window_rect.height

#  Setup font
font_size = 124
font = pygame.font.SysFont(None, font_size)

'''
    Which controller Selection Section
'''
picking_controller = True
selected_index = 0

controller_options = ["All"] + controllers_available
num_options = len(controller_options)
vertical_margin = font_size

available_menu_items_per_page = (window_height - vertical_margin * 2) / font_size

page_index_offset = 0

def render_menu():
    windowSurface.fill((0, 0, 0))
    #  Draw previous if needed
    if page_index_offset > 0:
        text = font.render("Previous", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = center_x
        textRect.y = 0 
        
        windowSurface.blit(text, textRect)
    #  Draw Next if needed
    if page_index_offset + available_menu_items_per_page < num_options:
        text = font.render("Next", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = center_x
        textRect.y = window_height - font_size

        windowSurface.blit(text, textRect)
    for i in range(min(num_options, available_menu_items_per_page, num_options-page_index_offset)):
        menu_index = i + page_index_offset

        if selected_index == i:
            text = font.render(controller_options[menu_index], True, (0, 255, 0), (0, 0, 0))
        else:
            text = font.render(controller_options[menu_index], True, (255, 255, 255), (0, 0, 0))
        
        textRect = text.get_rect()
        textRect.centerx = center_x
        textRect.y = i * font_size + vertical_margin
        
        windowSurface.blit(text, textRect)

    pygame.display.update()

#  Moving up on menu
def menu_up():
    global selected_index
    global page_index_offset
    
    if selected_index > 0:
        selected_index -= 1
    #  Wrap around
    else:
        if page_index_offset > 0:
            page_index_offset -= available_menu_items_per_page
        selected_index = available_menu_items_per_page - 1
    render_menu()

#  Moving down on menu
def menu_down():
    global selected_index
    global page_index_offset
    
    # how many items on this page?
    items_left = available_menu_items_per_page
    if available_menu_items_per_page > num_options - page_index_offset:
        items_left = num_options - page_index_offset
    
    if selected_index < items_left - 1:
        selected_index += 1
    #  Wrap Around or go to the next page
    else:
        if selected_index + page_index_offset  < num_options - 1:
            page_index_offset += available_menu_items_per_page
        selected_index = 0
    render_menu()

render_menu()
while picking_controller:
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYUP:
                #  Up Arrow or W
                if event.key == 273 or event.key == 119:
                    menu_up()
                elif event.key == 274 or event.key == 115:
                    menu_down()
                #  Enter Key
                elif event.key == 13:
                    picking_controller = False
            elif event.type == JOYBUTTONUP:
                if event.button == 1:
                    picking_controller = False
            
            elif event.type == JOYHATMOTION:
                if event.value[1] == 1:
                    menu_up()
                elif event.value[1] == -1:
                    menu_down()
            elif event.type == JOYAXISMOTION:
                #  ignore really small presses
                if abs(event.value) < 0.1:
                    continue
                if event.axis == 1:
                    if event.value < 0:
                        menu_up()
                    elif event.value > 0:
                        menu_down()

if selected_index + page_index_offset == 0:
    controllers = controllers_available
else:
    controllers = [controller_options[selected_index + page_index_offset]]     
'''
    Controller confguration section
'''
def render():  
    windowSurface.fill((0, 0, 0))
    
    #  Display controller image
    windowSurface.blit(controllerImage, controllerImageRect)

    #  Display the controller label
    text = font.render("Controller: " + controller['name'], True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = center_x
    textRect.centery = controllerImageRect[1] - font_size/2
    windowSurface.blit(text, textRect)
    
    #  Display what button we're currently configuring
    key_text = font.render("Currently configuring button: "+ buttons_to_update[current_button], True, (255, 255, 255), (0, 0, 0))
    currentTextRect = key_text.get_rect()
    currentTextRect.centerx = windowSurface.get_rect().centerx
    currentTextRect.centery = controllerImageRect[1] + controllerImageRect[3] + font_size/2
    windowSurface.blit(key_text, currentTextRect) 
    
    pygame.display.update()

for selected_controller in controllers:
    #  Read in controller data
    input_path = DIRECTORY + "controllers/" + selected_controller
    try:
        input_text = open(input_path + "/info.json").read()
    except:
        print "Invalid controller: %s. Skipping" % selected_controller
        continue
    controller = json.loads(input_text)

    #  Load controller image
    controllerImage = pygame.image.load(input_path + '/'+controller['image']).convert()

    #  Setup where controller image will be drawn
    controllerImageRect = controllerImage.get_rect()
    controllerImageRect.centerx = center_x
    controllerImageRect.centery = center_y

    #  Which button are we adjusting?
    current_button = 0
    buttons_to_update = controller['controls']
    '''
        KEYUP = scancode, key, mod
        JOYBUTTONUP = joy, button
        JOYHATMOTION = joy, hat, value
    '''

    mapping = {}
    running = True
    render()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type in events_to_capture:
                if event.type == KEYUP:
                    mapping[buttons_to_update[current_button]] = {"type":event.type, "key":event.key, "mod": event.mod}
                
                elif event.type == JOYBUTTONUP:
                    mapping[buttons_to_update[current_button]] = {"type":event.type, "button":event.button, "joy": event.joy}
                
                elif event.type == JOYHATMOTION:
                    #  Skip the event of the joystick reseting to 0, 0
                    if event.value == (0,0):
                        continue
                    mapping[buttons_to_update[current_button]] = {"type": event.type, "value": event.value, "joy": event.joy}
                
                elif event.type == JOYAXISMOTION:
                    #  Skip if the press wasn't 'hard' enough
                    if event.value < 1.0 and event.value > -1.0:
                        continue
                    mapping[buttons_to_update[current_button]] = {"type": event.type, "value": event.value, "axis": event.axis, "joy": event.joy}
                
                #  Advance to next button
                current_button += 1
                if current_button >= len(buttons_to_update):
                    current_button = 0
                    running = False
                else:
                    render()

    #  Output our mapping
    with open(controller['name'] + ".json", "w") as output_file:
        output_file.write(json.dumps(mapping, indent=4, separators=(',', ': ')))

    output_directory = []
    if "output_directory" in controller:
        for od in controller['output_directory']:
            output_directory.append(od)
    else:
        output_directory = "output/"+controller['name'] +"/"+formatter[:-3]

    #print output_directory
    count = 0
    #  Call Formatters
    if "formatters" in controller:
        for formatter in controller['formatters']:
            print formatter
            #print sys.executable, "formatters/"+formatter, controller['name'] + ".json ", output_directory[count]
            print output_directory[count]
	    try:
                pid = os.system('python ' + DIRECTORY +  "formatters/"+formatter + " " + controller['name'] + ".json " + output_directory[count] )
                #print pid
            except Exception as e:
                print e.message, e.args
                print formatter + " has failed."
            count += 1
