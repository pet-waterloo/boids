import pygame
import random

import pygame.math as pgmath
import math

import soragl as SORA
from soragl import scene
from soragl import physics, base_objects, smath

from scripts import singleton

DISTANCE = 100
MAX_SPEED = 120


class Boid(physics.Entity):
    TYPE = "BOID"

    def __init__(self, x: int, y: int):
        super().__init__(Boid.TYPE)
        self.position = x, y
        self.velocity = smath.normalized_random_vec2() * (
            (random.random() - 0.5) * 40 + 80
        )
        self.n_vel = self.velocity.normalize()
        self.flow_angle = 0

    def on_ready(self):
        # create components
        self.add_component(base_objects.Script(self.script))
        self.add_component(base_objects.Collision2DComponent())

    def update(self):
        self.n_vel = self.velocity.normalize()
        if self.position.x > SORA.FSIZE[0]:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = SORA.FSIZE[0]
        if self.position.y > SORA.FSIZE[1]:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = SORA.FSIZE[1]

        # print(0 < self.position.x < SORA.FSIZE[0] and 0 < self.position.y < SORA.FSIZE[1])

    def script(self):
        pygame.draw.circle(SORA.FRAMEBUFFER, (255, 255, 255), self.position, 1)
        # draw velocity vector
        cx = int(60*math.sin(self.position.x * SORA.DELTA)) + 120
        cy = int(30 * math.cos(self.position.y * SORA.DELTA)) + 190
        pygame.draw.line(
            SORA.FRAMEBUFFER,
            (cx, cy, 250 - cx),
            self.position,
            self.position + self.velocity.normalize() * 10,
        )
        perp_vel = self.n_vel.rotate(90) * 5
        pygame.draw.line(
            SORA.FRAMEBUFFER,
            (cx, cy, 250-cx),
            self.position + perp_vel + self.n_vel * 2,
            self.position - perp_vel + self.n_vel * 2,
        )

        # if self._entity_id in [1, 2]:
        #     print(f"Entity ID: {self._entity_id} | {self.c_chunk}")

        # properties to sum

        vel_sum = pgmath.Vector2(self.n_vel)
        cohesion_sum = pgmath.Vector2(self.n_vel)
        separation_sum = pgmath.Vector2(self.n_vel)

        # time to draw lines
        for dx, dy in [
            (-1, 1),
            (0, 1),
            (1, 1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ]:
            # connect with other particles
            nx, ny = self.c_chunk[0] + dx, self.c_chunk[1] + dy
            cc = self.world.get_chunk(nx, ny)
            for e in cc._intrinstic_entities:
                if e[1] is self._entity_id:
                    continue
                # create a weighted movement vector
                off = e[0].position - self.position
                dis = off.magnitude()
                if dis > DISTANCE:
                    continue
                vel_sum += e[0].n_vel * dis_weight_func_vel(dis)
                cohesion_sum += off * dis_weight_func_coh(dis)
                separation_sum += off * dis_weight_func_sep(dis)
                if self._entity_id == 1:
                    # draw lines to nearby entities
                    # continue
                    pygame.draw.line(
                        SORA.FRAMEBUFFER,
                        (255, 255, 255),
                        self.position,
                        e[0].position,
                    )

        # add weighted properties
        self.velocity += (
            (vel_sum.normalize() * 4 + cohesion_sum.normalize() * 2 + separation_sum.normalize() * 2) * SORA.DELTA * 60
        )
        self.velocity.xy = smath.__clamp__(self.velocity.x, -MAX_SPEED, MAX_SPEED), smath.__clamp__(
            self.velocity.y, -MAX_SPEED, MAX_SPEED
        )
        self.flow_angle += (random.random() * 10 - 5) * SORA.DELTA
        self.flow_angle = smath.__clamp__(self.flow_angle, -2, 2)
        self.flow_angle *= 0.98
        # TODO: add rotation
        self.velocity = self.velocity.rotate(self.flow_angle)
        self.velocity *= 0.94

    def debug(self, surface):
        pass

    def kill(self):
        super().kill()


def w_func(d: float):
    return (10 * d) / (d * d + 100)

# custom weight functions
def dis_weight_func_vel(d: float):
    return 1/ (d/10 + 3) 

def dis_weight_func_coh(d: float):
    return w_func(d-10)/3

def dis_weight_func_sep(d: float):
    return -w_func(d + 20) / 2
