from GameObjects import *

pygame.init()

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
clock = pygame.time.Clock()

player = Player(DISP_WIDTH // 2, DISP_HEIGHT // 2)
room = Room(map)
game_mode = '2d'
mini_map = pygame.Surface((DISP_WIDTH // 3, DISP_HEIGHT // 3))
mini_map.set_alpha(200)
tick = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if game_mode == '2d':
                    game_mode = '3d'
                else:
                    game_mode = '2d'

    display.fill('black')


    if game_mode == '2d':
        room.draw(display)
        room.raycasting(player, display, game_mode)
        player.draw(display)
    else:
        pygame.draw.rect(display, 'lightblue', (0, 0, DISP_WIDTH, DISP_HEIGHT // 2))
        pygame.draw.rect(display, 'darkgray', (0, DISP_HEIGHT // 2, DISP_WIDTH, DISP_HEIGHT))
        mini_map.fill('black')
        room.draw(mini_map, 3)
        room.raycasting(player, display, game_mode)
        display.blit(mini_map, (0, DISP_HEIGHT * 2 // 3))
        player.draw(mini_map, 3)
    room.physics(player)

    player.move()
    mouse_pos = pygame.mouse.get_pos()
    if DISP_WIDTH - mouse_pos[0] <= 30:
        pygame.mouse.set_pos((35, mouse_pos[1]))
    elif mouse_pos[0] <= 30:
        pygame.mouse.set_pos((DISP_WIDTH - 35, mouse_pos[1]))

    pygame.display.update()
    clock.tick(60)
    tick += 1
    if not tick % 100:
        print(pygame.mouse.get_rel())