import pygame
import random

import soragl as SORA
from soragl import physics, base_objects


class Boid(physics.Entity):
    TYPE = "BOID"

    def __init__(self, x: int, y: int):
        super().__init__(Boid.TYPE)
        self.position = x, y
        self.velocity = random.random(), random.random()

    def on_ready(self):
        # create components
        self.add_component(base_objects.Script(self.script))

    def update(self):
        self.position += self.velocity

    def script(self):
        pygame.draw.circle(SORA.FRAMEBUFFER, (255, 255, 255), self.position, 2)

    def debug(self, surface):
        pass

    def kill(self):
        super().kill()
