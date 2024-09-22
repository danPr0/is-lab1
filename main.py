import pygame
import sys

from settings import HEIGHT, NAV_HEIGHT, WIDTH
from world import World


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.fps = pygame.time.Clock()

    def main(self):
        world = World(self.screen)
        while True:
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            world.update()
            pygame.display.update()
            self.fps.tick(30)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
    pygame.display.set_caption('PacMan')

    play = Main(screen)
    play.main()
