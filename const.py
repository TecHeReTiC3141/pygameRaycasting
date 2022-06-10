from math import *
import pygame

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 1280, 720
WALL_HEIGHT = DISP_HEIGHT - 100
WALL_SIZE = 100

FOV = pi / 3
NUM_RAYS = 320
MAX_DEPTH = 800
SCALE = DISP_WIDTH // NUM_RAYS
SCREEN_DIST = NUM_RAYS / (2 * tan(FOV / 2))
PROJ_COEFF = SCREEN_DIST * WALL_HEIGHT

font = pygame.font.SysFont('Arial', 30)

map = [
    '#############',
    '#.#.###.##..#',
    '#...###.#...#',
    '#..##.......#',
    '#.......#...#',
    '#.......#...#',
    '#############'
]