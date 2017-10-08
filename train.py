import pygame, sys
from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
LANE_COLOR = (0, 0, 255)
GREEN = (0, 255, 0)
LANED_COLOR = (0, 0, 0)
LANE_WIDTH = WINDOW_WIDTH / 15

def main():
    pygame.init()
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    windowSurface.fill(WHITE)
    area = 0
    pygame.draw.rect(windowSurface, GREEN, (0, 0, WINDOW_WIDTH/3.5, WINDOW_HEIGHT))
    area += WINDOW_WIDTH/3.5
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, LANED_COLOR, (area, 0, LANE_WIDTH / 10, WINDOW_HEIGHT))
    area += LANE_WIDTH / 10
    pygame.draw.rect(windowSurface, LANE_COLOR, (area, 0, LANE_WIDTH, WINDOW_HEIGHT))
    area += LANE_WIDTH
    pygame.draw.rect(windowSurface, GREEN, (area, 0, WINDOW_WIDTH / 3.5, WINDOW_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()