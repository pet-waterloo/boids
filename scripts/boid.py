import pygame
import random

import pygame.math as pgmath

import soragl as SORA
from soragl import physics, base_objects, smath

from scripts import singleton


class Boid(physics.Entity):
    TYPE = "BOID"

    def __init__(self, x: int, y: int):
        super().__init__(Boid.TYPE)
        self.position = x, y
        self.velocity = smath.normalized_random_vec2() * (
            (random.random() - 0.5) * 40 + 80
        )
        self.n_vel = self.velocity.normalize()

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
        pygame.draw.line(
            SORA.FRAMEBUFFER,
            (255, 0, 0),
            self.position,
            self.position + self.velocity.normalize() * 10,
        )

        # if self._entity_id in [1, 2]:
        #     print(f"Entity ID: {self._entity_id} | {self.c_chunk}")

        # properties to sum

        vel_sum = pgmath.Vector2(0, 0)

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
                dis = (e[0].position - self.position).magnitude()
                if dis > 50: continue
                vel_sum += e[0].n_vel * dis_weight_func(dis)
                if self._entity_id == 1:
                    # draw lines to nearby entities
                    pygame.draw.line(
                        SORA.FRAMEBUFFER,
                        (255, 255, 255),
                        self.position,
                        e[0].position,
                    )

        # add weighted properties
        self.velocity += vel_sum * SORA.DELTA * 30
        self.velocity.xy = smath.__clamp__(self.velocity.x, -100, 100), smath.__clamp__(
            self.velocity.y, -100, 100
        )

    def debug(self, surface):
        pass

    def kill(self):
        super().kill()


# custom weight functions
def dis_weight_func(d: float):
    return 1 / (d / 10 + 2.7)
