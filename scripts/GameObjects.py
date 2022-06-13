from scripts.const import *


class Player:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.surf = pygame.Surface((50, 50))
        self.surf.set_colorkey('black')
        self.cur_rect = self.surf.get_rect(center=(x, y))
        self.prev_rect = self.surf.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def draw(self, display: pygame.Surface, coef=1):
        pygame.draw.circle(display, 'green', (self.cur_rect.centerx // coef,
                                              self.cur_rect.centery // coef), 25 // coef)
        pygame.draw.line(display, 'red', (self.cur_rect.centerx // coef,
                                          self.cur_rect.centery // coef),
                         ((self.cur_rect.centerx + 50 * cos(self.angle)) // coef,
                          (self.cur_rect.centery + 50 * sin(self.angle)) // coef), width=5)

    def move(self):
        self.prev_rect = self.cur_rect.copy()
        move = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        sin_a, cos_a = sin(self.angle), cos(self.angle)
        if keys[pygame.K_a]:
            move.x += sin_a
            move.y += -cos_a
        if keys[pygame.K_d]:
            move.x += -sin_a
            move.y += cos_a
        if keys[pygame.K_w]:
            move.x += cos_a
            move.y += sin_a
        if keys[pygame.K_s]:
            move.x += -cos_a
            move.y += -sin_a

        mouse_x_move = pygame.mouse.get_rel()[0]
        self.angle += mouse_x_move / 800
        if keys[pygame.K_LEFT]:
            self.angle -= .03
        if keys[pygame.K_RIGHT]:
            self.angle += .03
        self.angle %= pi * 2

        self.cur_rect.move_ip(move * self.speed)


class Wall:
    textures = {
        '1': stone_wall1,
        '2': stone_wall2
    }

    def __init__(self, x, y, text_ind, width=WALL_SIZE, height=WALL_SIZE):
        self.cur_rect = pygame.Rect(x * WALL_SIZE, y * WALL_SIZE, width, height)
        self.texture = self.textures[text_ind]

    def draw(self, display: pygame.Surface, coef=1):

        pygame.draw.rect(display, 'darkgreen', (self.cur_rect.left // coef,
                                                self.cur_rect.top // coef,
                                                self.cur_rect.width // coef,
                                                self.cur_rect.height // coef,))

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


class Sprite(Wall):
    sprite = pygame.Surface((50, 50))
    is_obst = True

    def __init__(self, x, y, v_shift, scale):
        self.x, self.y = x * WALL_SIZE, y * WALL_SIZE
        self.rect = pygame.Rect(x, y, WALL_SIZE, WALL_SIZE)
        self.scale = scale
        self.v_shift = v_shift

    def collide(self, entity: Player):
        if not self.is_obst:
            return
        super().collide(entity)

    def obj_locate(self, player: Player, walls: list):
        dx, dy = self.x - player.x, self.y - player.y
        dist_to_sprite = sqrt(dx ** 2 + dy ** 2)

        sprite_angle = atan2(dy, dx)
        gamma = sprite_angle - player.angle
        if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += 2 * pi

        delta_rays = gamma // DELTA_ANGLE
        cur_ray = NUM_RAYS // 2 - 1 + delta_rays
        dist_to_sprite *= cos(FOV // 2 - cur_ray * DELTA_ANGLE)

        if 0 <= cur_ray < NUM_RAYS and dist_to_sprite < walls[cur_ray][0]:
            proj_height = int(PROJ_COEFF // dist_to_sprite * self.scale)
            half_height = proj_height // 2
            shift = half_height * self.v_shift

            sprite_pos = (cur_ray * SCALE - half_height,
                          DISP_HEIGHT // 2 - half_height + shift)
            sprite = pygame.transform.scale(self.sprite, (proj_height, proj_height))

            return dist_to_sprite, sprite, sprite_pos
        return False,


class Torch(Sprite):
    pass


class Barrel(Sprite):
    sprite = pygame.image.load('../sprites/barrel.png')


class Room:

    def __init__(self, map: list[str]):
        self.walls = []
        self.sprites = [
            Barrel(11.5, 3.5, 1.8, 0.8),
            Barrel(11.5, 7.5, 1.8, 1.1),
        ]
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] != '.':
                    self.walls.append(Wall(j, i, map[i][j]))

    def draw(self, display: pygame.Surface, coef=1):
        for wall in self.walls:
            wall.draw(display, coef)

    def physics(self, entity: Player):
        for wall in self.walls:
            wall.collide(entity)

    @staticmethod
    def mapping(x, y) -> tuple:
        return (x // WALL_SIZE) * WALL_SIZE, (y // WALL_SIZE) * WALL_SIZE

    def raycasting(self, player: Player, display: pygame.Surface,
                   game_mode: str):
        obj_to_draw = []
        x0, y0 = player.cur_rect.center
        xm, ym = self.mapping(*player.cur_rect.center)
        cur_ang = player.angle - FOV / 2
        for ray in range(NUM_RAYS):
            sin_r, cos_r = sin(cur_ang), cos(cur_ang)

            # horizontal
            hory, dy = (ym + WALL_SIZE, 1) if sin_r >= 0 else (ym, -1)
            for i in range(0, DISP_HEIGHT, WALL_SIZE):
                depth_h = (hory - y0) / sin_r
                horx = x0 + depth_h * cos_r

                stop = False
                for wall in self.walls:
                    if wall.cur_rect.collidepoint(horx, hory + dy):
                        stop = True
                        wall_h_texture = wall.texture
                        break
                if stop:
                    break

                hory += WALL_SIZE * dy

            # vert
            vertx, dx = (xm + WALL_SIZE, 1) if cos_r >= 0 else (xm, -1)
            for i in range(0, DISP_WIDTH, WALL_SIZE):
                depth_v = (vertx - x0) / cos_r
                verty = y0 + depth_v * sin_r
                stop = False
                for wall in self.walls:
                    if wall.cur_rect.collidepoint(vertx + dx, verty):
                        stop = True
                        wall_v_texture = wall.texture
                        break
                if stop:
                    break
                vertx += WALL_SIZE * dx

            mi_depth, offset, texture = (depth_v, int(verty), wall_v_texture) \
                if depth_v < depth_h else (depth_h, int(horx), wall_h_texture)
            offset %= WALL_SIZE

            if mi_depth < MAX_DEPTH and game_mode == '3d':
                mi_depth *= cos(player.angle - cur_ang)
                obst_height = PROJ_COEFF / mi_depth

                wall_slice = texture.subsurface(offset * TEXTURE_SCALE, 0,
                                                TEXTURE_SCALE, texture.get_height())
                wall_slice = pygame.transform.scale(wall_slice, (SCALE, obst_height))
                wall_pos = (ray * SCALE, DISP_HEIGHT // 2 - obst_height // 2)

                obj_to_draw.append((mi_depth, wall_slice, wall_pos))

            elif game_mode == '2d':
                x, y = x0 + min(mi_depth, MAX_DEPTH) * cos_r, \
                       y0 + min(mi_depth, MAX_DEPTH) * sin_r
                pygame.draw.line(display, 'darkgray',
                                 player.cur_rect.center, (x, y))

            cur_ang += FOV / NUM_RAYS

        return obj_to_draw
