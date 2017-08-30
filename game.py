import pygame
import random
import sys
import os
import time
from pygame.locals import *
from threading import Timer
import inputbox

# @@@@@@@@@@@@@@@@@@@@
# ==== GLOBAL VAR ====
# @@@@@@@@@@@@@@@@@@@@

# USER CHANGE VARIABLES
LANE_NO = random.randrange(1, 7)  # player spawn lane
LANES_LEFT = 1
LANES_RIGHT = 1
BLOCKS_AHEAD = 1
BLOCKS_BEHIND = 1

# GUI VARIABLES
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TEXT_COLOR = (0, 0, 255)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)
LANE_COLOR = (128, 128, 128)
LANED_COLOR = (0, 0, 0)
FPS = 60

# CNN VARIABLES
REWARD = 0  # cars passed
LIFE = 1
LEFT = 1
FORWARD = 2
RIGHT = 3
TRAFFIC_MIN_SPEED = 10
TRAFFIC_MAX_SPEED = 50
LANE_WIDTH = WINDOW_WIDTH / 15
CAR_SPEED = 30
result = {'left': LEFT, 'forward': FORWARD, 'right': RIGHT}
init = 0
lane1 = []
lane2 = []
lane3 = []
lane4 = []
lane5 = []
lane6 = []


# @@@@@@@@@@@@@@@@@
# === FUNCTIONS ===
# @@@@@@@@@@@@@@@@@

def game_end():
    pygame.quit()
    sys.exit()


def is_key_pressed():
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_t):
                return 1
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_p):
                return 2
            if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                game_end()


def text_display(text, fonts, surface, x, y, text_color, background_color):
    text_obj = fonts.render(text, 1, text_color, background_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def collision(player, traffic_cars):
    for car in traffic_cars:
        if player != car:
            print "player : ", player['lane']
            print "car : ", car['lane']
            if player['rect'].colliderect(car['rect']):
                return True
    return False


def t_collision(some_car, traffic_cars):
    for a_car in traffic_cars:
        if a_car['lane'] == some_car['lane'] and a_car['speed'] != some_car['speed']:
            if a_car['collision_rect'][0].colliderect(some_car['collision_rect'][1]) or \
                    a_car['collision_rect'][1].colliderect(some_car['collision_rect'][0]):
                if a_car['speed'] > some_car['speed']:
                    a_car['speed'] = some_car['speed']
                else:
                    some_car['speed'] = a_car['speed']


# Draw the game world on the window.
def gui(area):
    global LANE_NO, lane1, lane2, lane3, lane4, lane5, lane6, init, player_car

    pygame.draw.rect(windowSurface, GREEN, (0, 0, WINDOW_WIDTH / 3.5, WINDOW_HEIGHT))
    area += WINDOW_WIDTH / 3.5
    lane1 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane1.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    lane2 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane2.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    lane3 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane3.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    lane4 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane4.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    lane5 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane5.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    lane6 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane6.append(area)

    pygame.draw.rect(windowSurface, GREEN, (area, 0, WINDOW_WIDTH / 3.5, WINDOW_HEIGHT))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ========= MAIN GAME =========
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# initialize the game
pygame.init()
# start the main clock
mainClock = pygame.time.Clock()
# set display window size
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# window game title
pygame.display.set_caption('Self driving CAR')
# mouse cursor visibility : ON
pygame.mouse.set_visible(True)

# **************
# LOADING STUFF
# **************

# FONTS
font = pygame.font.SysFont(None, 30)
font1 = pygame.font.SysFont(None, 60)

# IMAGES
player_image = pygame.image.load('image/car1.png')
car2 = pygame.image.load('image/car2.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = player_image.get_rect()
sample = [car2, car3, car4]

# ***************
#  START SCREEN
# ***************

windowSurface.fill(BACKGROUND_COLOR)
# image display background
background_img = pygame.image.load('image/back.png')
# put up the image at x,y
windowSurface.blit(background_img, (20, 20))

# heading text
text_display("SELF DRIVING CAR", font1, windowSurface, (WINDOW_WIDTH / 3) - 60, (WINDOW_HEIGHT / 15),
             (0, 0, 255), (255, 255, 0))

# image display speedometer logo
logo_img = pygame.image.load('image/logo.png')
# put up the image at x,y
windowSurface.blit(logo_img, (330, 130))

# image display car logo
logo_img = pygame.image.load('image/car.png')
# put up the image at x,y
windowSurface.blit(logo_img, (30, 330))

# text to hint for game start
text_display("Press 'T' : Start Self - drive", font, windowSurface, (WINDOW_WIDTH / 1.75) - 10,
             (3 * (WINDOW_HEIGHT / 4) + 10), (0, 200, 0), BACKGROUND_COLOR)
text_display("Press 'P' : Play the game to train", font, windowSurface, (WINDOW_WIDTH / 1.75) - 10,
             (3 * (WINDOW_HEIGHT / 4) + 40), (0, 200, 0), BACKGROUND_COLOR)

player_name = inputbox.ask(windowSurface, "Player Name")
# update frames on the screen after event input
pygame.display.update()
# check if user is generating any event, wait endlessly
choice = is_key_pressed()
# score in file for initialization
zero = 0
top_speed = zero

# @@@@ FEED SCORE @@@@
if not os.path.exists("data/save.dat"):
    f = open("data/save.dat", 'w')
    data = player_name + " : " + str(zero)
    f.write(data)
    f.close()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Start the game if user hits the choice key
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

while LIFE > 0:
    # list for all cars
    cars = []
    prev_lane = 0
    spawn_car = 0
    area = 0
    gui(area)
    # draw the lanes
    link_dict = {1: lane1, 2: lane2, 3: lane3, 4: lane4, 5: lane5, 6: lane6}

    # player car attributes
    player_car = {'collision_rect': [pygame.Rect(int(link_dict[LANE_NO][0]) + 10, (WINDOW_HEIGHT / 2) - 30, 30, 15),
                                     pygame.Rect(int(link_dict[LANE_NO][0]) + 10, (WINDOW_HEIGHT / 2) + 65, 30, 15)],
                  'self_rect': pygame.Rect(int(link_dict[LANE_NO][0]) + 10, WINDOW_HEIGHT / 2, 30, 60),
                  'speed': CAR_SPEED / 5,
                  'surface': pygame.transform.scale(player_image, (30, 60)),
                  'lane': LANE_NO}

    # GAME LOOP
    while True:
        gui(area)
        # Draw the score and top score.
        text_display('REWARD: %s' % REWARD, font, windowSurface, 10, 20, (255, 0, 0), (255, 255, 255))
        text_display('SPEED: %s' % CAR_SPEED, font, windowSurface, 10, 50, (255, 0, 255), (255, 255, 255))
        text_display('Top Speed: %s' % top_speed, font, windowSurface, 10, 100, (255, 255, 255), (0, 0, 0))
        text_display('Remaining Lives: %s' % LIFE, font, windowSurface, 10, 130, (255, 255, 255), (0, 0, 0))

        # add new cars at the top of the screen
        if len(cars) < random.randrange(1, 6):
            temp = random.randrange(1, 7)
            if temp != prev_lane and temp != LANE_NO and prev_lane != LANE_NO:
                new_car = {'collision_rect': [pygame.Rect(int(link_dict[temp][0]) + 10, -61, 30, 15),
                                              pygame.Rect(int(link_dict[temp][0]) + 10, 0, 30, 15)],
                           'self_rect': pygame.Rect(int(link_dict[temp][0]) + 10, -60, 30, 60),
                           'speed': random.randint(TRAFFIC_MIN_SPEED / 5, TRAFFIC_MAX_SPEED / 5),
                           'surface': pygame.transform.scale(random.choice(sample), (30, 60)),
                           'lane': temp}
                cars.append(new_car)
            prev_lane = temp

        # if the player wants to train the car
        if choice == 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    LIFE = LIFE - 1

            if LIFE==0:
                break

            if player_car['self_rect'].bottom < 0:
                player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)
            for c in cars:
                c['collision_rect'][1].move_ip(0, c['speed'])
                c['self_rect'].move_ip(0, c['speed'])
                c['collision_rect'][0].move_ip(0, c['speed'])
                t_collision(c, cars)

            for c in cars:
                if c['self_rect'].top > WINDOW_HEIGHT or c['speed'] > player_car['speed']:
                    cars.remove(c)

            # display the cars
            windowSurface.blit(player_image, player_car['self_rect'])
            for c in cars:
                windowSurface.blit(c['surface'], c['self_rect'])

            # update/refresh the display
            pygame.display.update()

        # if the player wants to drive the car
        elif choice == 2:
            for event in pygame.event.get():
                if event.type == K_UP:
                    CAR_SPEED = CAR_SPEED + 1
                if event.type == K_DOWN:
                    CAR_SPEED = CAR_SPEED - 1
                if event.type == K_LEFT:
                    CAR_SPEED = CAR_SPEED + 1
                if event.type == K_RIGHT:
                    CAR_SPEED = CAR_SPEED + 1
                if event.type == QUIT:
                    LIFE = LIFE - 1

            if LIFE==0:
                break

            if player_car['self_rect'].bottom < 0:
                player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)
            for c in cars:
                c['collision_rect'][1].move_ip(0, c['speed'])
                c['self_rect'].move_ip(0, c['speed'])
                c['collision_rect'][0].move_ip(0, c['speed'])
                t_collision(c, cars)

            player_car['self_rect'].move_ip(0, -CAR_SPEED)
            for c in cars:
                if c['self_rect'].top > WINDOW_HEIGHT or c['speed'] > player_car['speed']:
                    cars.remove(c)

            # display the cars
            windowSurface.blit(player_image, player_car['self_rect'])
            for c in cars:
                windowSurface.blit(c['surface'], c['self_rect'])

            # update/refresh the display
            pygame.display.update()

        mainClock.tick(FPS)

    # ***************
    #  END SCREEN
    # ***************
    v = open("data/save.dat", 'r')
    speed_data = v.readline().split()
    top_speed = int(speed_data[2])
    v.close()
    time.sleep(1)
    if LIFE == 0:
        text_display('!! ~~ Game over ~~ !!', font1, windowSurface, (WINDOW_WIDTH / 4) - 10, (WINDOW_HEIGHT / 3),
                     (0, 0, 0), (255, 255, 255))
        text_display('Press esc key to QUIT', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 2),
                     (0, 0, 255), (255, 255, 0))
        text_display('Press p to play again', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 4),
                     (0, 0, 255), (255, 255, 0))
        pygame.display.update()
        time.sleep(2)
        choice1 = is_key_pressed()
        if choice1 == 2:
            LIFE = 1

