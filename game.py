import pygame
import pygame_gui
import main_menu
import constants
import numpy
import rocket
import asteroid
from game_states import GAME_STATES

background_color = (0, 0, 0)


def ingame(surface: pygame.surface.Surface):
    asteroid_count = 4
    clock = pygame.time.Clock()
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    score = 0
    score_img = font.render(
        str(score), True, (200, 200, 200), background_color)
    score_rect = score_img.get_rect()
    score_rect.topright = (constants.window_width - 30, 30)
    asteroids_group = pygame.sprite.Group()
    asteroids_group.add(asteroid.asteroid(asteroid_count, numpy.array(
        (0, constants.window_height*0.33)), constants.generalise_height(constants.asteroid_radius), [constants.asteroid_start_vel, 0]))
    asteroids_group.add(asteroid.asteroid(asteroid_count, numpy.array(
        (0, constants.window_height*0.66)), constants.generalise_height(constants.asteroid_radius), [constants.asteroid_start_vel, 0]))
    asteroids_group.add(asteroid.asteroid(asteroid_count, numpy.array(
        (constants.window_width, constants.window_height*0.33)), constants.generalise_height(constants.asteroid_radius), [-constants.asteroid_start_vel, 0]))
    asteroids_group.add(asteroid.asteroid(asteroid_count, numpy.array(
        (constants.window_width, constants.window_height*0.66)), constants.generalise_height(constants.asteroid_radius), [-constants.asteroid_start_vel, 0]))

    player = rocket.rocket()
    respawn_start_ticks = pygame.time.get_ticks()
    respawning = False
    bullets = []

    is_running = True
    while is_running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    ret = pause_menu(surface)
                    if ret != GAME_STATES.IN_GAME:
                        return ret
        if player.status == rocket.ROCKET_STATUS.DEAD:
            return game_over_menu(surface)

        surface.fill(background_color)
        # Might need to change next line to copy asteroid group
        asteroids_group.update(asteroids_group, player, dt, bullets)
        dead_count = 0
        to_be_removed = []
        parent = asteroids_group.sprites()[0]
        for a in asteroids_group:
            if a.avg_dist_samples > parent.avg_dist_samples:
                parent = a
        for ast in asteroids_group:
            if ast.status == asteroid.ASTEROID_STATUS.DESTROYED:
                asteroids_group.remove(ast)
                to_be_removed.append(ast)
        for r in to_be_removed:
            asteroids_group.remove(r)
            tmp_start_vel = [0, 0]
            tmp_start_pos = [0, 0]
            if numpy.random.random() < 0.5:
                tmp_start_pos = [0, constants.window_height * numpy.random.random()]
                tmp_start_vel = [constants.asteroid_start_vel, 0]
            else:
                tmp_start_pos = [constants.window_width, constants.window_height * numpy.random.random()]
                tmp_start_vel = [-constants.asteroid_start_vel, 0]
            tmp = asteroid.asteroid(asteroid_count, numpy.array(tmp_start_pos), constants.generalise_height(constants.asteroid_radius), numpy.array(tmp_start_vel))
            tmp.evolve_from(parent)
            asteroids_group.add(tmp)
            dead_count += 1
            score += 1
            score_img = font.render(
                str(score), True, (200, 200, 200), background_color)
            score_rect = score_img.get_rect()
            score_rect.topright = (constants.window_width-30, 30)

        # if dead_count == asteroid_count:
        #     if not respawning:
        #         print("INFO: All dead")
        #         respawning = True
        #         respawn_start_ticks = pygame.time.get_ticks()
        #     else:
        #         if (pygame.time.get_ticks() - respawn_start_ticks)/1000.0 >= 0.0001:
        #             print("INFO: Respawning:", pygame.time.get_ticks())
        #             parent = None
        #             parent_index = 0
        #             for i in range(0, asteroid_count):
        #                 if asteroids_group.sprites()[i].avg_dist_samples < asteroids_group.sprites()[parent_index].avg_dist_samples:
        #                     parent_index = i
        #             parent = asteroids_group.sprites()[parent_index]
        #             asteroids_group.empty()
        #             tmp = asteroid.asteroid(asteroid_count, numpy.array(
        #                 (0, constants.window_height*0.33)), constants.generalise_height(constants.asteroid_radius), [constants.asteroid_start_vel, 0.0])
        #             tmp.evolve_from(parent)
        #             asteroids_group.add(tmp)
        #             tmp = asteroid.asteroid(asteroid_count, numpy.array(
        #                 (0, constants.window_height*0.66)), constants.generalise_height(constants.asteroid_radius), [constants.asteroid_start_vel, 0.0])
        #             tmp.evolve_from(parent)
        #             asteroids_group.add(tmp)
        #             tmp = asteroid.asteroid(asteroid_count, numpy.array(
        #                 (constants.window_width, constants.window_height*0.5)), constants.generalise_height(constants.asteroid_radius), [-constants.asteroid_start_vel, 0.0])
        #             tmp.evolve_from(parent)
        #             asteroids_group.add(tmp)
        #             tmp = asteroid.asteroid(asteroid_count, numpy.array(
        #                 (constants.window_width, constants.window_height*0.5)), constants.generalise_height(constants.asteroid_radius), [-constants.asteroid_start_vel, 0.0])
        #             tmp.evolve_from(parent)
        #             asteroids_group.add(tmp)

        #             score += 1
        #             score_img = font.render(
        #                 str(score), True, (200, 200, 200), background_color)
        #             score_rect = score_img.get_rect()
        #             score_rect.topright = (constants.window_width-30, 30)
        #             respawning = False
        player.update(asteroids_group, dt, bullets)
        to_be_removed = []
        for i in range(0, len(bullets)):
            bullets[i].update(dt)
            pos = bullets[i].position
            if pos[0] < 0 or pos[0] > constants.window_width or pos[1] < 0 or pos[1] > constants.window_height:
                to_be_removed.append(i)
            bullets[i].draw(surface)
        for i in to_be_removed:
            bullets.pop(i)
        asteroids_group.draw(surface)
        surface.blit(player.image, player.rect)
        surface.blit(score_img, score_rect)

        pygame.display.update()


def pause_menu(surface: pygame.surface.Surface):
    menu_rect = pygame.rect.Rect((constants.window_width//4, constants.window_width//4),
                                 (constants.window_width//2, constants.window_height//2))
    menu_rect.center = (constants.window_width//2, constants.window_height//2)
    paused_background = (50, 50, 50)
    paused_foreground = (200, 200, 200)

    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font("ARCADECLASSIC.TTF",
                            constants.generalise_height(75))
    pause_img = font.render("game paused", True,
                            paused_foreground, paused_background)
    pause_rect = pause_img.get_rect()
    pause_rect.center = (constants.generalise_width(640),
                         constants.generalise_height(292))

    resume_button_rect = pygame.Rect((constants.generalise_width(549), constants.generalise_height(
        350)), (constants.generalise_width(164), constants.generalise_height(41)))
    quit_button_rect = pygame.Rect((constants.generalise_width(549), constants.generalise_height(
        409)), (constants.generalise_width(164), constants.generalise_height(41)))
    menu_button_rect = pygame.Rect((constants.generalise_width(549), constants.generalise_height(
        468)), (constants.generalise_width(164), constants.generalise_height(41)))

    resume_button = pygame_gui.elements.UIButton(
        relative_rect=resume_button_rect, text="Resume", manager=gui_manager)
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=quit_button_rect, text="Quit", manager=gui_manager)
    menu_button = pygame_gui.elements.UIButton(
        relative_rect=menu_button_rect, text="Exit to menu", manager=gui_manager)

    is_paused = True
    while is_paused:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == quit_button:
                        print("INFO: Quitting from pause menu")
                        return GAME_STATES.QUIT
                    if event.ui_element == resume_button:
                        print("INFO: Resuming game")
                        return GAME_STATES.IN_GAME
                    if event.ui_element == menu_button:
                        print("INFO: Exiting to main menu")
                        return GAME_STATES.MAIN_MENU

            gui_manager.process_events(event)

        gui_manager.update(dt)

        surface.fill(paused_background, menu_rect)
        surface.blit(pause_img, pause_rect)
        gui_manager.draw_ui(surface)

        pygame.display.update(menu_rect)


def game_over_menu(surface: pygame.surface.Surface):
    menu_rect = pygame.rect.Rect((constants.window_width//4, constants.window_height//4),
                                 (constants.window_width//2, constants.window_height//2))

    over_background = (200, 200, 200)
    over_foreground = (50, 50, 50)

    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height))

    clock = pygame.time.Clock()

    print("INFO: Game Over")
    return GAME_STATES.MAIN_MENU
    # font = pygame.font.Font("ARCADECLASSIC.TTF", 72
