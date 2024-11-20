import pygame
from settings import RES
from game import snake_game
from textures import update_config
if __name__ == "__main__":
    pygame.init()
    update_config()
    screen = pygame.display.set_mode((RES, RES))
    while True:
        if not snake_game(screen):
            break
