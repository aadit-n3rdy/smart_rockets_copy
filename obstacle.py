import numpy as np

class obstacle:
    position = []
    radius: float

    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
