from GameObjects import *
from Drawing import Drawing

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('3D-Raycasting')
clock = pygame.time.Clock()

player = Player(DISP_WIDTH // 2, DISP_HEIGHT // 2)
room = Room(map)
game_mode = '3d'
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
        room.raycasting(player, display, game_mode)
        player.draw(display)

    else:
        draw.background(player)
        mini_map.fill('black')
        room.draw(mini_map, 4)
        walls = room.raycasting(player, display, game_mode)
        draw.draw_objects(walls + [obj.obj_locate(player, walls) for obj in room.sprites])
        player.draw(mini_map, 4)
        display.blit(mini_map, (0, DISP_HEIGHT * 3 // 4))

    draw.display_info(clock, player)

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
