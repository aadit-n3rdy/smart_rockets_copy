#!/usr/bin/env python3
import pygame as pg
from game_states import GAME_STATES
import main_menu
import game
from constants import window_height, window_width

pg.init()
screen_size = (window_width, window_height)
surface = pg.display.set_mode(screen_size)

game_state = GAME_STATES.MAIN_MENU

while game_state != GAME_STATES.QUIT:
    if game_state == GAME_STATES.MAIN_MENU:
        game_state = main_menu.main_menu(surface)
    elif game_state == GAME_STATES.IN_GAME:
        game_state = game.ingame(surface)

pg.quit()
# rocket_img = pg.transform.smoothscale(pg.image.load(
#     'rocket.png').convert_alpha(), (253//4, 439//4))
# obstacle_img = pg.transform.smoothscale(
#     pg.image.load('obstacle.png').convert_alpha(), (200, 200))
# obst = obstacle([window_width//2, window_height//2], 50)
# rockets = []
# tmp = rocket(1)
# rockets.append(tmp)
# tmp = rocket(1)
# rockets.append(tmp)
# tmp = rocket(1)
# rockets.append(tmp)

# done = False
# print(rockets[1].network.weights)
# if rockets[0].network.weights[0].flat[0] == rockets[1].network.weights[0].flat[0]:
#     print("ERROR: STUPID WEIGHTS ARE EQUAL")
# while not done:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             done = True
#     screen.fill((25, 25, 25))
#     for rocket in rockets:
#         rocket_rotated_img = pg.transform.rotate(
#             rocket_img, rocket.angle - np.pi/2.0)
#         rocket_rect = rocket_rotated_img.get_rect(
#             center=(rocket.position[0], rocket.position[1]))
#         screen.blit(rocket_rotated_img, rocket_rect)
#         rocket.update([obst], 0.1)
#     obstacle_rect = obstacle_img.get_rect(
#         center=(obst.position[0], obst.position[1]))
#     # new_rect = new_rect.move(angle*0.1, angle*0.1)
#     screen.blit(obstacle_img, obstacle_rect)
#     pg.display.flip()


