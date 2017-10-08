# @@@@@@@@@@@@@@@@@@@@
# ===== PACKAGES =====
# @@@@@@@@@@@@@@@@@@@@

# python GUI game creation
import pygame
from pygame.locals import *
# use compiler/code core resource management
import sys
# seeding and random number generation
import random
# access to file management in OS

import os
# use clock and timers
import time
# python 3.5 version of multi-threading
import _thread
# google API for machine learning
import tensorflow as tf
# append a new path for local .py import
sys.path.append(r"D:/STUDY/PYTHON/self-driving-car-game/inputbox.py")
# input text box
import inputbox
import csv

# @@@@@@@@@@@@@@@@@@@@
# ==== GLOBAL VAR ====
# @@@@@@@@@@@@@@@@@@@@

# USER CHANGE VARIABLES (alter these to change the player car knowledge)
LIFE = 1 # number of turns to play
LANES_LEFT = 1
LANES_RIGHT = 1
BLOCKS_AHEAD = 1
BLOCKS_BEHIND = 1

# GUI & GAME VARIABLES (don't change, as window size affects everything)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LANE_WIDTH = int(WINDOW_WIDTH / 15)
TEXT_COLOR = (0, 0, 255)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)
LANE_COLOR = (128, 128, 128)
LANED_COLOR = (0, 0, 0)
FPS = 30 # game refresh rate

LANE_NO = random.randrange(1, 7)  # player spawn lane
TRAFFIC_MIN_SPEED = 10
TRAFFIC_MAX_SPEED = 50
CAR_SPEED = 0
CAR_SPEED2 = 1
prev_lane = LANE_NO
lane1 = []
lane2 = []
lane3 = []
lane4 = []
lane5 = []
lane6 = []
direction = 0
change_in_speed = 0
cnt = 0
count = 0
index = 0
file_name = "mat"
file_name += str(index)
path = "data/"+file_name+".csv"
knowledge = []
keystroke = [0,0,0,0,0]

# CNN VARIABLES
REWARD = 0  # cars passed (may be positive or negative)
LEFT = 1  # output to take left
ACCEL = 2  # output to increase speed
RIGHT = 3  # output to take right
BRAKE = 4  # output to decrease speed

# @@@@@@@@@@@@@@@@@
# === FUNCTIONS ===
# @@@@@@@@@@@@@@@@@


# add new cars in the traffic car dictionary
def add_car():
    if len(cars) < random.randrange(1, 9):
        temp = random.randrange(1, 7)
        global direction
        direction = random.randrange(0, 2)
        # spawn cars above the map and player car
        if direction == 0:
            new_car = {'collision_rect': [pygame.Rect(int(link_dict[temp][0]) + 10, -116, 30, 30),
                                          pygame.Rect(int(link_dict[temp][0]) + 10, -40, 30, 30)],
                       'self_rect': pygame.Rect(int(link_dict[temp][0]) + 10, -100, 30 , 60),
                       'speed': random.randint(int(TRAFFIC_MIN_SPEED / 5), int(TRAFFIC_MAX_SPEED / 5)),
                       'surface': pygame.transform.scale(random.choice(sample), (30, 60)),
                       'lane': temp,
                       'direction': direction,
                       'rel_pos': "",
                       'stat': ""}
        # spawn cars below the map and player car
        elif direction == 1:
            new_car = {'collision_rect': [pygame.Rect(int(link_dict[temp][0]) + 10, 640, 30, 30),
                                          pygame.Rect(int(link_dict[temp][0]) + 10, 717, 30, 30)],
                       'self_rect': pygame.Rect(int(link_dict[temp][0]) + 10, 656, 30, 60),
                       'speed': random.randint(int(TRAFFIC_MIN_SPEED / 5), int(TRAFFIC_MAX_SPEED / 5)),
                       'surface': pygame.transform.scale(random.choice(sample), (30, 60)),
                       'lane': temp,
                       'direction': direction,
                       'rel_pos': "",
                       'stat': ""}
        cars.append(new_car)

# First thread : creates cars every 0.5 seconds
def update1(tname, delay):
    while True:
        time.sleep(delay)
        add_car()


# Second thread : removes cars if not in the map every 3 seconds
def update2(tname, delay):
    while True:
        time.sleep(delay)
        # delete new cars not in the screen
        for c in cars:
            # remove cars below
            if (c['self_rect'].top > WINDOW_HEIGHT) and (abs(c['self_rect'].top - player_car['self_rect'].top) > WINDOW_HEIGHT) and ((c['rel_pos'] == "below") or (c['rel_pos'] == "approaching")):
                cars.remove(c)
            # remove cars above
            if c['self_rect'].bottom < 0 and (abs(c['self_rect'].top - player_car['self_rect'].top) > WINDOW_HEIGHT) and ((c['rel_pos'] == "above") or (c['rel_pos'] == "receding")):
                cars.remove(c)


# Third thread : calculates the reward of the car every 0.01
def update3(tname, delay):
    while True:
        time.sleep(delay)
        global REWARD, file_name, path
        # add new cars at the top of the screen
        for c in cars:
            if c['speed'] >= player_car['speed']:
                if c['self_rect'].top < player_car['self_rect'].top:
                    if c['rel_pos'] == "approaching":
                        REWARD -= 1
                        c['rel_pos'] = "above"
                    elif c['rel_pos'] == "":
                        c['rel_pos'] = "above"
                elif c['self_rect'].top > player_car['self_rect'].top:
                    c['rel_pos'] = "approaching"
            elif c['speed'] <= player_car['speed']:
                if c['self_rect'].top < player_car['self_rect'].top:
                    c['rel_pos'] = "receding"
                elif c['self_rect'].top > player_car['self_rect'].top:
                    if c['rel_pos'] == "receding":
                        REWARD += 1
                        c['rel_pos'] = "below"
                    elif c['rel_pos'] == "":
                        c['rel_pos'] = "below"


# Second thread : removes cars if not in the map every 3 seconds
def count_timer(tname, delay):
    while True:
        time.sleep(delay)
        global cnt
        cnt += 1

# Quit the game
def game_end():
    pygame.quit()
    sys.exit()


# check if user has pressed any functional keys
def is_key_pressed():
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s):
                return 1
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_t):
                return 2
            if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                game_end()


# display custom formatted texts from a few options
def text_display(text, fonts, surface, x, y, text_color, background_color):
    text_obj = fonts.render(text, 1, text_color, background_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# check collision of player car and traffic cars
def p_collision(player, traffic_cars):
    for car in traffic_cars:
        if player['self_rect'].colliderect(car['self_rect']):
            return True
    return False


# check collision of traffic cars internally
# intelligence to traffic cars to stop if accident possibility ahead
def t_collision(some_car, traffic_cars):
    for a_car in traffic_cars:
        if a_car['lane'] == some_car['lane'] and a_car['speed'] != some_car['speed']:
            if (a_car['collision_rect'][0].colliderect(some_car['collision_rect'][1])) or (some_car['collision_rect'][1].colliderect(a_car['collision_rect'][0])):
                a_car['speed'] = some_car['speed']
            elif (a_car['collision_rect'][1].colliderect(some_car['collision_rect'][0])) or (some_car['collision_rect'][0].colliderect(a_car['collision_rect'][1])):
                some_car['speed'] = a_car['speed']


# check collision of traffic cars with collision matrix
def k_collision(tname, delay):
    while True:
        global count, keystroke
        time.sleep(delay)
        is_empty_knowledge_area = True

        for i in range(0, BLOCKS_AHEAD + BLOCKS_BEHIND + 2):
            for j in range(0, LANES_LEFT + LANES_RIGHT + 1):
                knowledge_matrix[i][j] = 0

        for car in cars:
            if ((car['self_rect'].top >= collision_matrix[0][0][1]) and (car['self_rect'].top <= collision_matrix[BLOCKS_BEHIND+BLOCKS_AHEAD+1][0][1] + 30)) and ((car['self_rect'].right > collision_matrix[0][0][0]) and (car['self_rect'].left < collision_matrix[0][LANES_LEFT+LANES_RIGHT][0] + 30)):
                # print("car in knowledge area")
                is_empty_knowledge_area = False
                for i in range(0, BLOCKS_AHEAD + BLOCKS_BEHIND + 2):
                    for j in range(0, LANES_LEFT + LANES_RIGHT + 1):
                        if ((car['self_rect'].top >= collision_matrix[i][j][1]) and (car['self_rect'].top <= collision_matrix[i][j][1] + 30)) and ((car['self_rect'].right > collision_matrix[i][j][0]) and (car['self_rect'].left < collision_matrix[i][j][0] + 30)):
                            knowledge_matrix[i][j] = 1
                        if ((car['self_rect'].center[1] >= collision_matrix[i][j][1]) and (
                            car['self_rect'].center[1] <= collision_matrix[i][j][1] + 30)) and (
                            (car['self_rect'].right > collision_matrix[i][j][0]) and (
                            car['self_rect'].left < collision_matrix[i][j][0] + 30)):
                            knowledge_matrix[i][j] = 1
                knowledge.append(str(knowledge_matrix) + str(keystroke))

        if is_empty_knowledge_area:
            knowledge.append(str(knowledge_matrix) + str(keystroke))

    # while True:
    #     global count, knowledge
    #     time.sleep(delay)
    #     for car in cars:
    #         for i in range(0, BLOCKS_AHEAD + BLOCKS_BEHIND + 2):
    #             for j in range(0, LANES_LEFT + LANES_RIGHT + 1):
    #                 if (car['stat'] == "") and ((car['self_rect'].top >= collision_matrix[i][j][1]) and (car['self_rect'].top <= collision_matrix[i][j][1] + 60)) and ((car['self_rect'].right > collision_matrix[i][j][0]) and (car['self_rect'].left < collision_matrix[i][j][0] + 30)):
    #                     knowledge_matrix[i][j] = 1
    #                     car['stat'] = "mc"
    #                 else:
    #                     knowledge_matrix[i][j] = 0
    #                 knowledge.append(str(knowledge_matrix[i][j]))
    #         if car['stat'] != "" and car['stat'] != "counted":
    #             count += 1
    #             print(count)
    #             car['stat'] = "counted"


# Draw the game world on the window.
def gui(area):
    global LANE_NO, lane1, lane2, lane3, lane4, lane5, lane6, player_car
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

if not os.path.exists(path):
    open(path, 'w')

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

# Creating threads as follows:
try:
    _thread.start_new_thread(update1, ("update_thread1", 0.5, ))
    _thread.start_new_thread(update2, ("update_thread2", 3, ))
    _thread.start_new_thread(update3, ("update_thread3", 0.01,))
    _thread.start_new_thread(count_timer, ("update_thread4", 0.2,))
    _thread.start_new_thread(k_collision, ("update_thread5", 0.01,))
    print("Success: Escape sequence initiated!")
except:
    print("Error: unable to start thread")

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Start the game if user hits the choice key
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# list for all cars
cars = []
area = 0
gui(area)
# draw the lanes
link_dict = {1: lane1, 2: lane2, 3: lane3, 4: lane4, 5: lane5, 6: lane6}

# player car attributes
player_car = {'collision_rect': [pygame.Rect(int(link_dict[LANE_NO][0]) + 10, (WINDOW_HEIGHT / 2) - 30, 30, 15),
                                 pygame.Rect(int(link_dict[LANE_NO][0]) + 10, (WINDOW_HEIGHT / 2) + 65, 30, 15)],
              'self_rect': pygame.Rect(int(link_dict[LANE_NO][0]) + 10, WINDOW_HEIGHT / 2, 30, 60),
              'speed': int((CAR_SPEED2 + CAR_SPEED) / 5),
              'surface': pygame.transform.scale(player_image, (30, 60)),
              'lane': LANE_NO}

collision_matrix = [[0 for x in range(LANES_RIGHT+LANES_LEFT+1)] for y in range(BLOCKS_AHEAD+BLOCKS_BEHIND+2)]
knowledge_matrix = [[0 for x in range(LANES_RIGHT+LANES_LEFT+1)] for y in range(BLOCKS_AHEAD+BLOCKS_BEHIND+2)]

while LIFE > 0:
    gui(area)
    # Draw the score and top score.
    display_speed = str(int((CAR_SPEED+CAR_SPEED2)/5))
    text_display('REWARD: %s' % REWARD, font, windowSurface, 10, 20, (255, 0, 0), (255, 255, 255))
    text_display('SPEED: %s' % display_speed, font, windowSurface, 10, 50, (255, 0, 255), (255, 255, 255))
    text_display('Remaining Lives: %s' % LIFE, font, windowSurface, 10, 130, (255, 255, 255), (0, 0, 0))

    # if the player wants to watch/test the trained car
    if choice == 1:
        global CAR_SPEED2
        CAR_SPEED2 = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                game_end()

        if LIFE == 0:
            break

        # if the player wants to watch/test the trained car
        if player_car['self_rect'].bottom < 0:
            player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)
            for c in cars:
                if c['direction'] == 0 and c['lane'] == LANE_NO:
                    c['collision_rect'][0].topleft = (link_dict[c['lane']][0] + 10, random.randint(0,WINDOW_HEIGHT - 200))
                    c['self_rect'].topleft = (link_dict[c['lane']][0] + 10, random.randint(0,WINDOW_HEIGHT - 200))
                    c['collision_rect'][1].topleft = (link_dict[c['lane']][0] + 10, random.randint(0,WINDOW_HEIGHT - 200))
                elif c['direction'] == 1:
                    c['collision_rect'][0].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT + 50)
                    c['self_rect'].topleft = (link_dict[c['lane']][0] + 10, c['self_rect'].topleft[1] + WINDOW_HEIGHT + 50)
                    c['collision_rect'][1].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT + 50)

        global direction
        for c in cars:
            c['collision_rect'][1].move_ip(0, -c['speed'])
            c['self_rect'].move_ip(0, -c['speed'])
            c['collision_rect'][0].move_ip(0, -c['speed'])
            t_collision(c, cars)

        # display the cars
        windowSurface.blit(player_image, player_car['self_rect'])
        for c in cars:
            windowSurface.blit(c['surface'], c['self_rect'])

        # update/refresh the display
        pygame.display.update()

    # if the player wants to drive and train the car
    elif choice == 2:
        global change_in_speed, CAR_SPEED, direction, cnt
        CAR_SPEED = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_UP):
                    change_in_speed = 0
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP):
                    change_in_speed = 0.2
                    keystroke = [0, 1, 0, 0, 0]
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN):
                    change_in_speed = -0.2
                    keystroke = [0, 0, 0, 1, 0]
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
                keystroke = [1, 0, 0, 0, 0]
                if player_car['lane'] > 1:
                    player_car['lane'] = player_car['lane'] - 1
                    LANE_NO = LANE_NO - 1
                    player_car['self_rect'].left = player_car['self_rect'].left - int(11*LANE_WIDTH/10)
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
                keystroke = [0, 0, 1, 0, 0]
                if player_car['lane'] < 6:
                    LANE_NO = LANE_NO + 1
                    player_car['lane'] = player_car['lane'] + 1
                    player_car['self_rect'].left = player_car['self_rect'].left + int(11*LANE_WIDTH/10)
            if event.type == QUIT:
                LIFE = LIFE - 1

        CAR_SPEED2 += change_in_speed
        if LIFE == 0:
            break

        for i in range(0, BLOCKS_AHEAD + BLOCKS_BEHIND + 2):
            for j in range(0, LANES_LEFT + LANES_RIGHT + 1):
                collision_matrix[i][j] = pygame.draw.rect(windowSurface, (255, 0, 0), (
                int(player_car['self_rect'].topleft[0] + 59 * j - 60 * LANES_LEFT),
                int(player_car['self_rect'].topleft[1]) + 30 * i - 30 * BLOCKS_AHEAD, 30, 30))

        if player_car['self_rect'].bottom < 0:
            player_car['self_rect'].topleft = (link_dict[LANE_NO][0] + 10, WINDOW_HEIGHT)
            for c in cars:
                if c['rel_pos'] == "" and direction == 0:
                    while True:
                        pos = random.randint(0, WINDOW_HEIGHT - 100)
                        flag = 0
                        for rcar in cars:
                            if pos >= rcar['self_rect'].top - 100 and pos <= rcar['self_rect'].bottom + 30 and c['lane']==rcar['lane']:
                                flag = 1
                        if flag == 0:
                            c['collision_rect'][0].topleft = (link_dict[c['lane']][0] + 10, pos - 30)
                            c['self_rect'].topleft = (link_dict[c['lane']][0] + 10, pos)
                            c['collision_rect'][1].topleft = (link_dict[c['lane']][0] + 10, pos + 60)
                            break
                        if cnt > 5:
                            cnt = 0
                            cars.remove(c)
                            break
                elif c['rel_pos'] == "above" or c['rel_pos'] == "receding":
                    c['collision_rect'][0].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT - 10)
                    c['self_rect'].topleft = (link_dict[c['lane']][0] + 10, c['self_rect'].topleft[1] + WINDOW_HEIGHT + 20)
                    c['collision_rect'][1].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT + 80)
                elif c['rel_pos'] == "below" or c['rel_pos'] == "approaching":
                    c['collision_rect'][0].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT + 20)
                    c['self_rect'].topleft = (link_dict[c['lane']][0] + 10, c['self_rect'].topleft[1] + WINDOW_HEIGHT + 50)
                    c['collision_rect'][1].topleft = (link_dict[c['lane']][0] + 10, c['collision_rect'][0].topleft[1] + WINDOW_HEIGHT + 110)


        for c in cars:
            c['collision_rect'][1].move_ip(0, -c['speed'])
            c['self_rect'].move_ip(0, -c['speed'])
            c['collision_rect'][0].move_ip(0, -c['speed'])
            t_collision(c, cars)
            if p_collision(player_car, cars):
                LIFE = LIFE - 1

        player_car['speed'] = int(CAR_SPEED2/5)
        player_car['self_rect'].move_ip(0, -player_car['speed'])

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

# print(count)
#writing to csv
with open(path, 'a') as train_data:
    file_writer = csv.writer(train_data, delimiter=',')
    for row in knowledge:
        input = []
        for c in row:
            if c == '0' or c == '1':
                input.append(c)
        file_writer.writerow(input)

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

# @@@@ FEED DATA @@@@
# with open("data/"+file_name+".csv", 'r') as f:
#     reader = csv.reader(f, delimiter=',')
#     for rows in reader:
#         for i in range(0,len(rows)):
#             print(rows[i])
#
