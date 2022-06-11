from math import *
import pygame
from pathlib import Path

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 1200, 720
WALL_HEIGHT = DISP_HEIGHT // 3
WALL_SIZE = 80

FOV = pi / 3
NUM_RAYS = 300
MAX_DEPTH = 1000
SCALE = DISP_WIDTH // NUM_RAYS
SCREEN_DIST = NUM_RAYS / (2 * tan(FOV / 2))
PROJ_COEFF = SCREEN_DIST * WALL_HEIGHT

font = pygame.font.SysFont('Arial', 30)

map = [
    '111111111122221',
    '1.1.111.12....1',
    '1...111.2.....1',
    '1..11.........1',
    '1.......2.....1',
    '1.......2.....1',
    '1.......2.....1',
    '1.......2.....1',
    '111111111111111'
]

TEXTURE_SIZE = (1200, 1200)
TEXTURE_SCALE = TEXTURE_SIZE[0] // WALL_SIZE
# textures
stone_wall1 = pygame.transform.scale(pygame.image.load('../textures/stone_wall.jpg'), TEXTURE_SIZE)
stone_wall2 = pygame.transform.scale(pygame.image.load('../textures/stone_wall2.jpg'), TEXTURE_SIZE)