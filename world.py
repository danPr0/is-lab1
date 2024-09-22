import pygame
import time
from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP, MAP_BINARY, PLAYER_SPEED
from pac import Pac
from cell import Cell
from berry import Berry
from maze import Maze
from ghost import Ghost
from display import Display


class World:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.maze = Maze(MAP_BINARY)
        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.reset_pos = False
        self.player_score = 0
        self.game_level = 3
        self._generate_world()

    # create and add player to the screen
    # noinspection PyTypeChecker
    def _generate_world(self):
        # renders obstacle from the MAP table
        for y_index, row in enumerate(MAP):
            for x_index, char in enumerate(row):
                if char == '1':  # for walls
                    self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
                elif char == ' ':  # for paths to be filled with berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == 'B':  # for big berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
                # for Ghosts's starting position
                elif char == 's':
                    self.ghosts.add(Ghost(x_index, y_index, 'skyblue', 'ahead'))
                elif char == 'p':
                    self.ghosts.add(Ghost(x_index, y_index, 'pink', 'ahead'))
                elif char == 'o':
                    self.ghosts.add(Ghost(x_index, y_index, 'orange', 'target'))
                elif char == 'r':
                    self.ghosts.add(Ghost(x_index, y_index, 'red', 'ahead'))
                # for PacMan's starting position
                elif char == 'P':
                    self.player.add(Pac(x_index, y_index))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    # noinspection PyTypeChecker
    def generate_new_level(self):
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == ' ':	 # for paths to be filled with berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == 'B':  # for big berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        time.sleep(2)

    def update(self):
        if not self.game_over:
            # player movement
            pressed_key = pygame.key.get_pressed()
            self.player.sprite.animate(pressed_key, self.walls_collide_list)
            # teleporting to the other side of the map
            if self.player.sprite.rect.left < 0 and self.player.sprite.moving_dir != 'right':
                self.player.sprite.rect.x = WIDTH + self.player.sprite.rect.left
            elif self.player.sprite.rect.right > WIDTH and self.player.sprite.moving_dir != 'left':
                self.player.sprite.rect.x = self.player.sprite.rect.right - WIDTH
            # PacMan eating-berry effect
            for berry in self.berries.sprites():
                if self.player.sprite.rect.colliderect(berry.rect):
                    if berry.power_up:
                        self.player.sprite.immune_time = 150  # Timer based from FPS count
                        self.player.sprite.pac_score += 50
                    else:
                        self.player.sprite.pac_score += 10
                    berry.kill()
            # PacMan bumping into ghosts
            for ghost in self.ghosts.sprites():
                if self.player.sprite.rect.colliderect(ghost.rect):
                    if not self.player.sprite.immune:
                        time.sleep(2)
                        self.player.sprite.life -= 1
                        self.reset_pos = True
                        break
                    else:
                        ghost.move_to_start_pos()
                        self.player.sprite.pac_score += 100
        self._check_game_state()
        # rendering
        for wall in self.walls.sprites():
            wall.update(self.screen)
        for berry in self.berries.sprites():
            berry.update(self.screen)
        for ghost in self.ghosts.sprites():
            ghost.update(self.game_level, self.walls_collide_list, self.maze, self.player.sprite.rect, self.player.sprite.moving_dir)
        self.ghosts.draw(self.screen)
        self.player.update()
        self.player.draw(self.screen)
        if self.game_over:
            self.display.game_over()
        self._refresh_dashboard()
        # reset Pac and Ghosts position after PacMan get captured
        if self.reset_pos and not self.game_over:
            [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
            self.player.sprite.move_to_start_pos()
            self.player.sprite.status = 'idle'
            self.player.sprite.direction = (0, 0)
            self.reset_pos = False
        # for restart button
        if self.game_over:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_r]:
                self.game_over = False
                self.restart_level()

    def _check_game_state(self):
        if self.player.sprite.life == 0:  # checks if game over
            self.game_over = True
        elif len(self.berries) == 0:  # generates new level
            self.game_level += 1
            for ghost in self.ghosts.sprites():
                ghost.move_speed += self.game_level
                ghost.move_to_start_pos()
            self.player.sprite.move_to_start_pos()
            self.player.sprite.direction = (0, 0)
            self.player.sprite.status = 'idle'
            self.generate_new_level()

    def restart_level(self):
        for ghost in self.ghosts.sprites():
            ghost.move_to_start_pos()
        self.berries.empty()
        self.game_level = 1
        self.player.sprite.pac_score = 0
        self.player.sprite.life = 3
        self.player.sprite.move_to_start_pos()
        self.player.sprite.direction = (0, 0)
        self.player.sprite.status = 'idle'
        self.generate_new_level()

    # displays nav
    def _refresh_dashboard(self):
        nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_HEIGHT)
        pygame.draw.rect(self.screen, pygame.Color('cornsilk4'), nav)

        self.display.show_life(self.player.sprite.life)
        self.display.show_level(self.game_level)
        self.display.show_score(self.player.sprite.pac_score)
