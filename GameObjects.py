import pygame
class Player:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.surf = pygame.Surface((50, 50))
        self.cur_rect = self.surf.get_rect(center=(x, y))
        self.prev_rect = self.surf.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def draw(self, display: pygame.Surface):
        pygame.draw.circle(self.surf, 'green', (25, 25), 25)
        display.blit(self.surf, self.cur_rect)

    def move(self):
        self.prev_rect = self.cur_rect.copy()
        move = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            move.x = -1
        if keys[pygame.K_d]:
            move.x = 1
        if keys[pygame.K_w]:
            move.y = -1
        if keys[pygame.K_s]:
            move.y = 1
        if keys[pygame.K_LEFT]:
            self.angle -= .02
        if keys[pygame.K_RIGHT]:
            self.angle += .02
        self.cur_rect.move_ip(move * self.speed )


class Wall:

    def __init__(self, x, y, width=50, height=50):
        self.cur_rect = pygame.Rect(x, y, width, height)

    def draw(self, display: pygame.Surface):
        pygame.draw.rect(display, 'white', self.cur_rect)
        pygame.draw.rect(display, 'black', self.cur_rect, width=5)

    def collide(self, entity: Player):
        if entity.cur_rect.colliderect(self.cur_rect):
            # left side
            if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                entity.cur_rect.right = self.cur_rect.left

            # right side
            elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                entity.cur_rect.left = self.cur_rect.right

                # top side
            if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                entity.cur_rect.bottom = self.cur_rect.top
            # bottom side
            elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                entity.cur_rect.top = self.cur_rect.bottom


class Room:

    def __init__(self, map: list[str]):

        self.walls = []
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == '#':
                    self.walls.append(Wall(j * 50, i * 50))

    def draw(self, display: pygame.Surface):
        for wall in self.walls:
            wall.draw(display)

    def physics(self, entity: Player):
        for wall in self.walls:
            wall.collide(entity)
