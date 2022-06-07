import pygame
from const import *
from GameObjects import *

pygame.init()

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
clock = pygame.time.Clock()

player = Player(DISP_WIDTH // 2, DISP_HEIGHT // 2)
room = Room(map)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display.fill('black')

    room.draw(display)
    room.physics(player)
    player.draw(display)
    player.move()

    pygame.display.update()
    clock.tick(60)