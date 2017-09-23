import pygame
import sys
import random
import os
import time
from pygame.locals import *
import _thread
import tensorflow as tf
sys.path.append(r"D:/STUDY/PYTHON/self-driving-car-game/inputbox.py")
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
FPS = 30

# CNN VARIABLES
REWARD = 0  # cars passed
LIFE = 1
LEFT = 1
FORWARD = 2
RIGHT = 3
TRAFFIC_MIN_SPEED = 10
TRAFFIC_MAX_SPEED = 50
LANE_WIDTH = int(WINDOW_WIDTH / 15)
CAR_SPEED = 30
CAR_SPEED2 = 1
result = {'left': LEFT, 'forward': FORWARD, 'right': RIGHT}
init = 0
prev_lane = LANE_NO
lane1 = []
lane2 = []
lane3 = []
lane4 = []
lane5 = []
lane6 = []
direction = 0
change_in_speed = 0
fl = 0
# @@@@@@@@@@@@@@@@@
# === FUNCTIONS ===
# @@@@@@@@@@@@@@@@@


def add_car():
    if len(cars) < random.randrange(1, 6):
        temp = random.randrange(1, 7)
        global direction
        direction = random.randrange(0, 2)
        if direction == 0:
            new_car = {'collision_rect': [pygame.Rect(int(link_dict[temp][0]) + 10, -116, 30, 30),
                                          pygame.Rect(int(link_dict[temp][0]) + 10, -40, 30, 30)],
                       'self_rect': pygame.Rect(int(link_dict[temp][0]) + 10, -100, 30 , 60),
                       'speed': CAR_SPEED/5 + CAR_SPEED2 - random.randint(int(TRAFFIC_MIN_SPEED / 6), int(TRAFFIC_MAX_SPEED / 6)),
                       'surface': pygame.transform.scale(random.choice(sample), (30, 60)),
                       'lane': temp,
                       'direction': direction,
                       'rel_pos' : ""}
        elif direction == 1:
            new_car = {'collision_rect': [pygame.Rect(int(link_dict[temp][0]) + 10, 640, 30, 30),
                                          pygame.Rect(int(link_dict[temp][0]) + 10, 717, 30, 30)],
                       'self_rect': pygame.Rect(int(link_dict[temp][0]) + 10, 656, 30, 60),
                       'speed': CAR_SPEED/5 + CAR_SPEED2 - random.randint(int(TRAFFIC_MIN_SPEED / 6), int(TRAFFIC_MAX_SPEED / 6)),
                       'surface': pygame.transform.scale(random.choice(sample), (30, 60)),
                       'lane': temp,
                       'direction': direction,
                       'rel_pos' : ""}
        cars.append(new_car)


# Define a function for the thread
def update(tname, delay):
    while True:
        time.sleep(delay)
        # add new cars at the top of the screen
        add_car()


def update2(tname, delay):
    while True:
        time.sleep(delay)
        # delete new cars not in the screen
        for c in cars:
            if c['self_rect'].top > WINDOW_HEIGHT and c['direction'] == 1:
                cars.remove(c)
            if c['self_rect'].bottom < 0 and c['direction'] == 0:
                cars.remove(c)


def update3(tname, delay):
    while True:
        global REWARD
        global fl
        time.sleep(delay)
        # add new cars at the top of the screen
        for c in cars:
            if (c['self_rect'].top > player_car['self_rect'].top) and (c['self_rect'].top < player_car['self_rect'].bottom) and (c['speed'] < 0):
                if c['rel_pos'] == "" or c['rel_pos'] == "behind":
                    REWARD -= 1
                    c['rel_pos'] = "ahead"
            if (c['self_rect'].bottom > player_car['self_rect'].top) and (c['self_rect'].bottom < player_car['self_rect'].bottom) and (c['speed'] > 0):
                if c['rel_pos'] == "" or c['self_rect'] == "ahead":
                    REWARD += 1
                    c['rel_pos'] = "behind"


def game_end():
    pygame.quit()
    sys.exit()


def is_key_pressed():
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s):
                return 1
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_t):
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
            if player['rect'].colliderect(car['rect']):
                return True
    return False


def t_collision(some_car, traffic_cars):
    for a_car in traffic_cars:
        if a_car['lane'] == some_car['lane'] and a_car['speed'] != some_car['speed']:
            if (a_car['collision_rect'][0].colliderect(some_car['collision_rect'][1])) or (some_car['collision_rect'][1].colliderect(a_car['collision_rect'][0])):
                a_car['speed'] = some_car['speed']
            elif (a_car['collision_rect'][1].colliderect(some_car['collision_rect'][0])) or (some_car['collision_rect'][0].colliderect(a_car['collision_rect'][1])):
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

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, int(LANE_WIDTH / 10), WINDOW_HEIGHT))
    area += int(LANE_WIDTH / 10)
    lane2 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane2.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, int(LANE_WIDTH / 10), WINDOW_HEIGHT))
    area += int(LANE_WIDTH / 10)
    lane3 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane3.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, int(LANE_WIDTH / 10), WINDOW_HEIGHT))
    area += int(LANE_WIDTH / 10)
    lane4 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane4.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, int(LANE_WIDTH / 10), WINDOW_HEIGHT))
    area += int(LANE_WIDTH / 10)
    lane5 = [area]

    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    lane5.append(area)

    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, int(LANE_WIDTH / 10), WINDOW_HEIGHT))
    area += int(LANE_WIDTH / 10)
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
text_display("Press 'S' : Start Self - drive", font, windowSurface, (WINDOW_WIDTH / 1.75) - 10,
             (3 * (WINDOW_HEIGHT / 4) + 10), (0, 200, 0), BACKGROUND_COLOR)
text_display("Press 'T' : Play the game to train", font, windowSurface, (WINDOW_WIDTH / 1.75) - 10,
             (3 * (WINDOW_HEIGHT / 4) + 40), (0, 200, 0), BACKGROUND_COLOR)

# update frames on the screen after event input
player_name = inputbox.ask(windowSurface, "Player Name")
pygame.display.update()
# check if user is generating any event, wait endlessly
choice = is_key_pressed()
# score in file for initialization
zero = 0
top_speed = zero

# Creating a thread as follows
try:
    print("Success: Escape sequence initiated!")
    _thread.start_new_thread(update, ("update_thread1", 0.5, ))
    _thread.start_new_thread(update2, ("update_thread2", 3, ))
    _thread.start_new_thread(update3, ("update_thread3", 0.1,))
except:
    print("Error: unable to start thread")

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
    spawn_car = 0
    area = 0
    gui(area)
    # draw the lanes
    # link_dict = {1: lane1, 2: lane2, 3: lane3, 4: lane4, 5: lane5, 6: lane6}
    # row_range = BLOCKS_AHEAD + BLOCKS_BEHIND + 2
    # col_range = LANES_LEFT + LANES_RIGHT + 1
    # collision_matrix = [[0 for x in range(row_range)] for y in range(col_range)]
    # for i in range(LANES_LEFT + LANES_RIGHT +1):
    #     for j in range(BLOCKS_AHEAD + BLOCKS_BEHIND + 2):
    #


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
        display_speed = str(int(CAR_SPEED+CAR_SPEED2))
        text_display('REWARD: %s' % REWARD, font, windowSurface, 10, 20, (255, 0, 0), (255, 255, 255))
        text_display('SPEED: %s' % display_speed, font, windowSurface, 10, 50, (255, 0, 255), (255, 255, 255))
        text_display('Top Speed: %s' % top_speed, font, windowSurface, 10, 100, (255, 255, 255), (0, 0, 0))
        text_display('Remaining Lives: %s' % LIFE, font, windowSurface, 10, 130, (255, 255, 255), (0, 0, 0))

        # if the player wants to train the car
        if choice == 1:
            CAR_SPEED2 = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    LIFE = LIFE - 1

            if LIFE == 0:
                break

            if player_car['self_rect'].bottom < 0:
                player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)

            global direction
            for c in cars:
                c['collision_rect'][1].move_ip(0, c['speed'])
                c['self_rect'].move_ip(0, c['speed'])
                c['collision_rect'][0].move_ip(0, c['speed'])
                t_collision(c, cars)
                if c['self_rect'].top > WINDOW_HEIGHT and c['direction'] == 0:
                    cars.remove(c)
                if c['self_rect'].bottom < 0 and c['direction'] == 1:
                    cars.remove(c)

            # display the cars
            windowSurface.blit(player_image, player_car['self_rect'])
            for c in cars:
                windowSurface.blit(c['surface'], c['self_rect'])

            # update/refresh the display
            pygame.display.update()

        # if the player wants to drive the car
        elif choice == 2:
            global change_in_speed
            CAR_SPEED = 0
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_DOWN) or (event.key == pygame.K_UP):
                        change_in_speed = 0
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP):
                        change_in_speed = 0.2
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN):
                        change_in_speed = -0.2
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
                    if player_car['lane'] > 1:
                        player_car['lane'] = player_car['lane'] - 1
                        LANE_NO = LANE_NO - 1
                        player_car['self_rect'].left = player_car['self_rect'].left - int(11*LANE_WIDTH/10)
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
                    if player_car['lane'] < 6:
                        LANE_NO = LANE_NO + 1
                        player_car['lane'] = player_car['lane'] + 1
                        player_car['self_rect'].left = player_car['self_rect'].left + int(11*LANE_WIDTH/10)

                if event.type == QUIT:
                    LIFE = LIFE - 1
            CAR_SPEED2 += change_in_speed
            for c in cars:
                c['speed'] = c['speed'] + change_in_speed
            if LIFE == 0:
                break

            if player_car['self_rect'].bottom < 0:
                player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)

            global direction
            for c in cars:
                c['collision_rect'][1].move_ip(0, c['speed'])
                c['self_rect'].move_ip(0, c['speed'])
                c['collision_rect'][0].move_ip(0, c['speed'])
                t_collision(c, cars)
                if c['self_rect'].top > WINDOW_HEIGHT and c['direction'] == 0:
                    cars.remove(c)
                if c['self_rect'].bottom < 0 and c['direction'] == 1:
                    cars.remove(c)

            player_car['self_rect'].move_ip(0, -CAR_SPEED2/5)

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
        text_display('Press s to play again', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 4),
                     (0, 0, 255), (255, 255, 0))
        pygame.display.update()
        time.sleep(2)
        choice1 = is_key_pressed()
        if choice1 == 2 or choice1 == 1:
            LIFE = 1