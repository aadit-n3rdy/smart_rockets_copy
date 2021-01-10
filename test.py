import pygame
import main_menu
import game
import constants

pygame.init()
surface = pygame.display.set_mode(size=(constants.window_width, constants.window_height))

game.ingame(surface)

game.pause_menu(surface)

main_menu.main_menu(surface)

