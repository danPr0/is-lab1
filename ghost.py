import pygame
import random
import time
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED
from maze import Maze


class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color, strategy):
        super().__init__()
        self.i = row
        self.j = col
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)
        self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        self.move_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.moving_dir = "up"
        self.img_path = f'assets/ghosts/{color}/'
        self.img_name = f'{self.moving_dir}.png'
        self.image_raw = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image_raw, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.directions = {
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
        }
        self.keys = ['left', 'right', 'up', 'down']
        self.direction = (0, 0)
        self.target = None
        self.strategy = strategy

    def _animate(self):
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def update(self, game_lvl, walls_collide_list, maze: Maze, pac_rect, pac_moving_dir):
        if game_lvl == 1:
            self.update_lvl_1(walls_collide_list)
        elif game_lvl == 2:
            self.update_lvl_2(maze, pac_rect, pac_moving_dir)
        else:
            self.update_lvl_3(walls_collide_list, maze, pac_rect, pac_moving_dir)

    def update_lvl_1(self, walls_collide_list):
        available_moves = []
        for key in self.keys:
            if not self.is_collide(*self.directions[key], walls_collide_list):
                available_moves.append(key)
        randomizing = False if len(available_moves) <= 2 and self.direction != (0, 0) else True
        # 60% chance of randomizing ghost move
        if randomizing and random.randrange(0, 100) <= 60:
            self.moving_dir = random.choice(available_moves)
            self.direction = self.directions[self.moving_dir]
        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)
        self._animate()

    def update_lvl_2(self, maze: Maze, pac_rect, pac_moving_dir):
        pac_i = pac_rect.y // CHAR_SIZE + (1 if pac_moving_dir == 'down' and pac_rect.y % CHAR_SIZE != 0 else 0)
        pac_j = pac_rect.x // CHAR_SIZE + (1 if pac_moving_dir == 'right' and pac_rect.x % CHAR_SIZE != 0 else 0)

        if self.rect.right <= 0 and self.moving_dir != 'right':
            self.rect.x = WIDTH - self.rect.right - self.rect.width
        if self.rect.left >= WIDTH and self.moving_dir != 'left':
            self.rect.x = self.rect.left - WIDTH
        # ghost_i = self.rect.y // CHAR_SIZE + (1 if self.moving_dir == 'up' and self.rect.y % CHAR_SIZE != 0 else 0)
        # ghost_j = (self.rect.x + (CHAR_SIZE if self.moving_dir == 'left' and self.rect.x % CHAR_SIZE != 0 else 0)) // CHAR_SIZE
        if self.rect.y % CHAR_SIZE == 0 and self.rect.x % CHAR_SIZE == 0:
            self.i = self.rect.y // CHAR_SIZE
            self.j = self.rect.x // CHAR_SIZE
            ghost_i = self.i
            ghost_j = self.j

            route = maze._calc_route(ghost_i, ghost_j, pac_i, pac_j)
            next_step_i, next_step_j = maze.decode_point(route[0])
            if (next_step_j < ghost_j and next_step_j != 0) or (ghost_j == 0 and next_step_j == WIDTH / CHAR_SIZE - 1):
                self.moving_dir = 'left'
            if (next_step_j > ghost_j and next_step_j != WIDTH / CHAR_SIZE - 1) or (ghost_j == WIDTH / CHAR_SIZE - 1 and next_step_j == 0):
                self.moving_dir = 'right'
            if next_step_i < ghost_i:
                self.moving_dir = 'up'
            if next_step_i > ghost_i:
                self.moving_dir = 'down'
            self.direction = self.directions[self.moving_dir]

        self.rect.move_ip(self.direction)
        self._animate()

    def update_lvl_3(self, walls_collide_list, maze: Maze, pac_rect, pac_moving_dir):
        pac_i = pac_rect.y // CHAR_SIZE + (1 if pac_moving_dir == 'down' and pac_rect.y % CHAR_SIZE != 0 else 0)
        pac_j = pac_rect.x // CHAR_SIZE + (1 if pac_moving_dir == 'right' and pac_rect.x % CHAR_SIZE != 0 else 0)

        if self.rect.right <= 0 and self.moving_dir != 'right':
            self.rect.x = WIDTH - self.rect.right - self.rect.width
        if self.rect.left >= WIDTH and self.moving_dir != 'left':
            self.rect.x = self.rect.left - WIDTH
        # ghost_i = self.rect.y // CHAR_SIZE + (1 if self.moving_dir == 'up' and self.rect.y % CHAR_SIZE != 0 else 0)
        # ghost_j = (self.rect.x + (CHAR_SIZE if self.moving_dir == 'left' and self.rect.x % CHAR_SIZE != 0 else 0)) // CHAR_SIZE
        if self.rect.y % CHAR_SIZE == 0 and self.rect.x % CHAR_SIZE == 0:
            self.i = self.rect.y // CHAR_SIZE
            self.j = self.rect.x // CHAR_SIZE
            ghost_i = self.i
            ghost_j = self.j

            route_to_pac = maze._calc_route(ghost_i, ghost_j, pac_i, pac_j)
            if self.strategy == 'ahead' and pac_moving_dir and len(route_to_pac) > 3:
                if random.random() > 0.7 or not self.target or maze.code_point(ghost_i, ghost_j) == self.target:
                    available_points = maze.get_available_points(pac_i, pac_j, pac_i - self.directions[pac_moving_dir][1] // self.move_speed, pac_j - self.directions[pac_moving_dir][0] // self.move_speed, 8, 5)
                    self.target = random.choice(available_points)
                route = maze._calc_route(ghost_i, ghost_j, *maze.decode_point(self.target))
            elif self.strategy == 'behind' and pac_moving_dir and len(route_to_pac) > 2:
                if random.random() > 0.85 or not self.target or maze.code_point(ghost_i, ghost_j) == self.target:
                    available_points = maze.get_available_points(pac_i, pac_j, pac_i + self.directions[pac_moving_dir][1] // self.move_speed, pac_j + self.directions[pac_moving_dir][0] // self.move_speed, 4, 2)
                    self.target = random.choice(available_points)
                route = maze._calc_route(ghost_i, ghost_j, *maze.decode_point(self.target))
            else:
                route = route_to_pac

            # if len(route_to_pac) > 5:
            #     if random.random() > 0.4 or not self.target or maze.code_point(ghost_i, ghost_j) == self.target:
            #         available_points = maze.get_available_points(pac_i, pac_j, 10)
            #         self.target = random.choice(available_points)
            #     target_i, target_j = maze.decode_point(self.target)
            #     if maze.matrix[target_i][target_j] != 1:
            #         pass
            #     route_to_pac = maze._calc_route(ghost_i, ghost_j, *maze.decode_point(self.target))

            if route:
                next_step_i, next_step_j = maze.decode_point(route[0])
                if (next_step_j < ghost_j and next_step_j != 0) or (ghost_j == 0 and next_step_j == WIDTH / CHAR_SIZE - 1):
                    self.moving_dir = 'left'
                if (next_step_j > ghost_j and next_step_j != WIDTH / CHAR_SIZE - 1) or (ghost_j == WIDTH / CHAR_SIZE - 1 and next_step_j == 0):
                    self.moving_dir = 'right'
                if next_step_i < ghost_i:
                    self.moving_dir = 'up'
                if next_step_i > ghost_i:
                    self.moving_dir = 'down'
                self.direction = self.directions[self.moving_dir]
        self.rect.move_ip(self.direction)

        self._animate()

    def is_collide(self, x, y, walls_collide_list):
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True

    def move_to_start_pos(self):
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
