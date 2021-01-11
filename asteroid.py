from neural_network import neural_network
import rocket
import numpy as np
import enum
from constants import *
import pygame
import bullet


class ASTEROID_STATUS(enum.Enum):
    ALIVE = 0
    DESTROYED = 1


class asteroid(pygame.sprite.Sprite):
    destroyed_by_player: bool
    network: neural_network = None
    position: np.array = None
    velocity: np.array = None
    status: ASTEROID_STATUS = ASTEROID_STATUS.ALIVE
    network_inp_count: int
    image: pygame.surface.Surface
    radius: float
    rect: pygame.rect.Rect
    avg_dist_sqrt: float
    avg_dist_samples: float
    last_avg_dist_sample_tick: float
    least_dist_sq: float

    def __init__(self, asteroid_count: int, start_position: np.array, radius: float, start_velocity):
        super().__init__()
        self.destroyed_by_player = False
        self.network_inp_count = 4
        self.network = neural_network([self.network_inp_count, 10, 10, 2])
        self.position = start_position.flat.copy()
        self.velocity = np.array(start_velocity)
        self.status = ASTEROID_STATUS.ALIVE
        self.image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('asteroid.png').convert_alpha(),
                                                                          (2*int(generalise_height(radius)), 2*int(generalise_height(radius)))), np.random.random()*360)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.least_dist_sq = 0
        self.last_avg_dist_sample_tick = pygame.time.get_ticks()
        self.avg_dist_samples = 0
        self.avg_dist_sqrt = 0

    def evolve_from(self, parent):
        self.network.from_parent(parent.network)

    def die(self):
        self.status = ASTEROID_STATUS.DESTROYED

    def update(self, asteroids: pygame.sprite.Group, player: rocket.rocket, dt: float, bullets: list):
        if self.status == ASTEROID_STATUS.ALIVE:
            inp = []
            # inp.append(self.position[0])
            # inp.append(self.position[1])
            inp.append(self.velocity[0])
            inp.append(self.velocity[1])
            inp.append(player.position[0] - self.position[0])
            inp.append(player.position[0] - self.position[0])
            out = self.network.calculate(np.array(inp))
            self.velocity[0] += out[0] * asteroid_accel_coeff * dt
            self.velocity[1] += out[1] * asteroid_accel_coeff * dt
            self.position[0] += out[0] * asteroid_vel_coeff * dt
            self.position[1] += out[1] * asteroid_vel_coeff * dt
            self.rect.center = (int(self.position[0]), int(self.position[1]))
            dx = player.position[0] - self.position[0]
            dy = player.position[1] - self.position[1]
            dist_sq = dx**2 + dy**2
            if dist_sq < self.least_dist_sq or self.least_dist_sq < 0:
                self.least_dist_sq = dist_sq
            asteroids.remove(self)
            for asteroid in asteroids:
                dx = asteroid.position[0] - self.position[0]
                dy = asteroid.position[1] - self.position[1]
                if dx**2 + dy**2 <= 4*(asteroid.radius+self.radius)**2:
                    self.die()
                    asteroids.add(self)
                    return
            asteroids.add(self)
            for bult in bullets:
                if self.rect.collidepoint(bult.position[0], bult.position[1]):
                    bullets.remove(bult)
                    self.destroyed_by_player = True
                    self.die()
                    return
            if (pygame.time.get_ticks() - self.last_avg_dist_sample_tick) / 1000 >= 0.01:
                dx = self.position[0] - target_position[0]
                dy = self.position[1] - target_position[1]
                total = self.avg_dist_sqrt * \
                    self.avg_dist_samples + (dx**2 + dy**2)**0.25
                self.avg_dist_samples += 1
                self.avg_dist_sqrt = total/self.avg_dist_samples
                self.last_avg_dist_sample_tick = pygame.time.get_ticks()
            if self.position[0] < 0-self.radius or self.position[0] > window_width+self.radius or self.position[1] < 0-self.radius or self.position[1] > window_height+self.radius:
                self.die()
                return

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.image.get_rect(
            center=(int(self.position[0]), int(self.position[1]))))
