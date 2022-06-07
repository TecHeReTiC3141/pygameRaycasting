from const import *


class Player:



    def __init__(self, x, y):
        self.x, self.y = x, y
        self.surf = pygame.Surface((50, 50))
        self.surf.set_colorkey('black')
        self.cur_rect = self.surf.get_rect(center=(x, y))
        self.prev_rect = self.surf.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0


    def draw(self, display: pygame.Surface):
        pygame.draw.circle(self.surf, 'green', (25, 25), 25)

        pygame.draw.line(display, 'green', self.cur_rect.center,
                         (self.cur_rect.centerx + DISP_WIDTH * math.cos(self.angle),
                          self.cur_rect.centery + DISP_HEIGHT * math.sin(self.angle)))
        display.blit(self.surf, self.cur_rect)



    def move(self):
        self.prev_rect = self.cur_rect.copy()
        move = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        if keys[pygame.K_a]:
            move.x = sin_a
            move.y = -cos_a
        if keys[pygame.K_d]:
            move.x = -sin_a
            move.y = cos_a
        if keys[pygame.K_w]:
            move.x = cos_a
            move.y = sin_a
        if keys[pygame.K_s]:
            move.x = -cos_a
            move.y = -sin_a
        if keys[pygame.K_LEFT]:
            self.angle -= .02
        if keys[pygame.K_RIGHT]:
            self.angle += .02
        self.cur_rect.move_ip(move * self.speed )


class Wall:

    def __init__(self, x, y, width=100, height=100):
        self.cur_rect = pygame.Rect(x, y, width, height)

    def draw(self, display: pygame.Surface):
        pygame.draw.rect(display, 'black', self.cur_rect)
        pygame.draw.rect(display, 'white', self.cur_rect, width=5)

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
                    self.walls.append(Wall(j * 100, i * 100))

    def draw(self, display: pygame.Surface):
        for wall in self.walls:
            wall.draw(display)

    def physics(self, entity: Player):
        for wall in self.walls:
            wall.collide(entity)

    def raycasting(self, player: Player, display: pygame.Surface):
        cur_ang = player.angle - FOV / 2
        for ray in range(NUM_RAYS):
            cur_ang += FOV / NUM_RAYS
            sin_r, cos_r = math.sin(cur_ang), math.cos(cur_ang)
            coll = False
            for depth in range(0, MAX_DEPTH, 10):
                x = player.cur_rect.centerx + depth * cos_r
                y = player.cur_rect.centery + depth * sin_r

                for wall in self.walls:
                    if wall.cur_rect.collidepoint((x, y)):
                        coll = True
                        break
                if coll:
                    break
                pygame.draw.line(display, 'darkgray',
                                player.cur_rect.center, (x, y))
