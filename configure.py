import json
import sys
import os
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.joystick.init()

#  What controller are we configuring?
selected_controller = 0
controllers_available = os.listdir('controllers')
#  Read in controller data
input_path = "controllers/"+controllers_available[selected_controller]
input_text = open(input_path + "/info.json").read()
controller = json.loads(input_text)

#  Initialize screen
windowSurface = pygame.display.set_mode((500, 400), 0, 32)

#  Setup font
font = pygame.font.SysFont(None, 24)


def render():  
    windowSurface.fill((0, 0, 0))
    #  Display controller image
    controllerImage=pygame.image.load(input_path + '/'+controller['image']).convert()
    windowSurface.blit(controllerImage, (0,0))

    text = font.render("Controller: " + controller['name'], True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    windowSurface.blit(text, textRect)
    
    key_text = font.render("Currently setting button: "+buttons_to_update[current_button], True, (255, 255, 255), (0, 0, 0))
    textRect = key_text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery + 48
    windowSurface.blit(key_text, textRect) 
    pygame.display.update()

#  Which button are we adjusting?
current_button = 0
buttons_to_update = controller['controls']
'''
    KEYUP = key, mod 
    JOYBUTTONUP = joy, button
    JOYHATMOTION = joy, hat, value
'''
events_to_capture = [KEYUP, JOYBUTTONUP, JOYHATMOTION]

mapping = {}
running = True
render()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type in events_to_capture:
            mapping[buttons_to_update[current_button]] = (event.type, event.key)
            current_button += 1
            if current_button >= len(buttons_to_update):
                current_button = 0
                running = False
            else:
                render()

print json.dumps(mapping)