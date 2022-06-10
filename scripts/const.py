from math import *
import pygame
from pathlib import Path

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 1280, 720
WALL_HEIGHT = DISP_HEIGHT // 3
WALL_SIZE = 80

FOV = pi / 3
NUM_RAYS = 320
MAX_DEPTH = 800
SCALE = DISP_WIDTH // NUM_RAYS
SCREEN_DIST = NUM_RAYS / (2 * tan(FOV / 2))
PROJ_COEFF = SCREEN_DIST * WALL_HEIGHT

font = pygame.font.SysFont('Arial', 30)

map = [
    '################',
    '#.#.###.##.....#',
    '#...###.#......#',
    '#..##..........#',
    '#.......#......#',
    '#.......#......#',
    '#.......#......#',
    '#.......#......#',
    '################'
]

#main_dir = Path('../../pygameRaycasting')

# sprites
stone_wall1 = pygame.image.load('../sprites/stone_wall.jpg')
stone_wall2 = pygame.image.load('../sprites/stone_wall2.jpg')