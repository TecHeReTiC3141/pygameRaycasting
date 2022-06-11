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
