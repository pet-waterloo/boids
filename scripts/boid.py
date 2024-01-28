import pygame

from engine.gamesystem import entity
from engine.misc import maths
from engine.handler import scenehandler, eventhandler
from engine import singleton as EGLOB




class Boid(entity.Entity):
    TYPE = "BOID"

    def __init__(self):
        super().__init__(Boid.TYPE)

    def start(self):
        # create components
        pass
    
    def update(self):
        pass

    def render(self, surface):
        pass

    def debug(self, surface):
        pass

    def kill(self):
        super().kill()




