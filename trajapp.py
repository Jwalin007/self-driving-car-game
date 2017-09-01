import pygame
import random
import sys
import os
import time
from pygame.locals import *
from threading import Timer
import inputbox

def app_end():
    pygame.quit()
    sys.exit()

def is_key_pressed():
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                return 1
            if event.type == pygame.QUIT:
                app_end()

def text_display(text, fonts, surface, x, y, text_color, background_color):
    text_obj = fonts.render(text, 1, text_color, background_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ========= MAIN GAME =========
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# initialize the game
pygame.init()
# start the main clock
mainClock = pygame.time.Clock()
# set display window size
windowSurface = pygame.display.set_mode((1366, 800))
# window game title
pygame.display.set_caption('Trajectory Calculator')
# mouse cursor visibility : ON
pygame.mouse.set_visible(True)

# ***************
#  START SCREEN
# ***************

windowSurface.fill((220, 220, 220))

while True:
    pygame.display.update()
    # check if user is generating any event, wait endlessly
    choice = is_key_pressed()