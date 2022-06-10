from GameObjects import *
from Drawing import Drawing

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('3D-Raycasting')
clock = pygame.time.Clock()

player = Player(DISP_WIDTH // 2, DISP_HEIGHT // 2)
room = Room(map)
game_mode = '2d'
mini_map = pygame.Surface((DISP_WIDTH // 4, DISP_HEIGHT // 4))
mini_map.set_alpha(200)
tick = 0

draw = Drawing(display)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                game_mode = '3d' if game_mode == '2d' else '2d'

    display.fill('black')

    if game_mode == '2d':
        room.draw(display)
        room.optim_raycasting(player, display, game_mode)
        player.draw(display)
    else:
        draw.background()
        mini_map.fill('black')
        room.draw(mini_map, 4)
        room.optim_raycasting(player, display, game_mode)

        player.draw(mini_map, 4)
        display.blit(mini_map, (0, DISP_HEIGHT * 3 // 4))

    display.blit(font.render(f'FPS: {round(clock.get_fps())}',
                             True, 'red'), (20, 20))
    display.blit(font.render(f'Angle: {round(degrees(player.angle))}',
                             True, 'red'), (220, 20))
    room.physics(player)
    player.move()

    pygame.display.update()
    clock.tick(60)
    tick += 1

    # updating cursor position
    mouse_pos = pygame.mouse.get_pos()
    if DISP_WIDTH - mouse_pos[0] <= 30:
        pygame.mouse.set_pos((35, mouse_pos[1]))
    elif mouse_pos[0] <= 30:
        pygame.mouse.set_pos((DISP_WIDTH - 35, mouse_pos[1]))
