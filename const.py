import math
import pygame

DISP_WIDTH, DISP_HEIGHT = 1280, 720

FOV = math.pi / 3
NUM_RAYS = 100
MAX_DEPTH = 600

map = [
    '#############',
    '#.#.###.##..#',
    '#...###.#...#',
    '#..##.......#',
    '#.......#...#',
    '#.......#...#',
    '#############'
]