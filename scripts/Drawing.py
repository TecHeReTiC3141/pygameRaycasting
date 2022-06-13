from GameObjects import *


# TODO implement dynamic sky
class Drawing:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.sky = pygame.transform.scale(pygame.image.load('../textures/sky.jpg'),
                                          (DISP_WIDTH, DISP_HEIGHT // 2))

    def background(self, player: Player):
        sky_offset = -5 * degrees(player.angle) % DISP_WIDTH
        self.surf.blit(self.sky, (sky_offset, 0))
        self.surf.blit(self.sky, (sky_offset - DISP_WIDTH, 0))
        self.surf.blit(self.sky, (sky_offset + DISP_WIDTH, 0))
        pygame.draw.rect(self.surf, 'darkgray', (0, DISP_HEIGHT // 2, DISP_WIDTH, DISP_HEIGHT))

    def draw_objects(self, objs: list[tuple]):
        for obj in sorted(objs, key=lambda i: -i[0]):
            if obj[0]:
                _, sprite, pos = obj
                self.surf.blit(sprite, pos)

    def display_info(self, clock: pygame.time.Clock, player: Player):
        self.surf.blit(font.render(f'FPS: {round(clock.get_fps())}',
                                 True, 'red'), (20, 20))
        self.surf.blit(font.render(f'Angle: {round(degrees(player.angle))}',
                                 True, 'red'), (220, 20))