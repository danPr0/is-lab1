import os

import pygame


def import_sprite(path):
    surface_list = []
    for img_path in os.listdir(path):
        full_path = os.path.join(path, img_path)
        img_surface = pygame.image.load(full_path).convert_alpha()
        surface_list.append(img_surface)
    return surface_list
