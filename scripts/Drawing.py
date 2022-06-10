from GameObjects import *

# TODO implement dynamic sky
class Drawing:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf

    def background(self):
        pygame.draw.rect(self.surf, 'lightblue', (0, 0, DISP_WIDTH, DISP_HEIGHT // 2))
        pygame.draw.rect(self.surf, 'darkgray', (0, DISP_HEIGHT // 2, DISP_WIDTH, DISP_HEIGHT))
