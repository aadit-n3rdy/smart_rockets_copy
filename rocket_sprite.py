import pygame
import numpy as np

class rocket_sprite(pygame.sprite.Sprite):
    super().__init__()

    self.image = pygame.transform.rotate(pygame.image.load('rocket.svg').convert_alpha(), -np.pi/2.0)
    
    
