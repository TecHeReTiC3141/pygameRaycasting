import math
import pygame

DISP_WIDTH, DISP_HEIGHT = 1280, 720
WALL_HEIGHT = DISP_HEIGHT - 100

FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = 640
SCALE = DISP_WIDTH // NUM_RAYS
SCREEN_DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
PROJ_COEFF = SCREEN_DIST * WALL_HEIGHT

map = [
    '#############',
    '#.#.###.##..#',
    '#...###.#...#',
    '#..##.......#',
    '#.......#...#',
    '#.......#...#',
    '#############'
]