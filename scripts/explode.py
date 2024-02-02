
import pygame
from pygame import math as pgmath
import random

import soragl as SORA
from soragl import signal, scene
from scripts import boid


class ExplodeSignalRegister(signal.SignalRegister):
    def __init__(self):
        super().__init__("explode")
    

class ExplodeReceiver(signal.Receiver):
    def __init__(self):
        super().__init__(self.explode_boids)

    def explode_boids(self, args: dict):
        # dict is empty
        if not scene.SceneHandler.CURRENT: 
            print(scene.SceneHandler.CURRENT)
            return
        # go through every single boid + set random velocity vector
        for layer in scene.SceneHandler.CURRENT._layers:
            for e in layer.iter_active_entities_filter_type(boid.Boid):
                # print(e)
                # reset velocity
                e.velocity = SORA.smath.normalized_random_vec2() * (
                    (random.random() - 0.5) * 40 + 80
                )
                # reset position
                e.position = pgmath.Vector2(
                    random.randint(0, SORA.FSIZE[0]),
                    random.randint(0, SORA.FSIZE[1]),
                )


