import pygame
import soragl as SORA
import struct

import random

from pygame import draw as pgdraw
from pygame import math as pgmath

from soragl import (
    animation,
    scene,
    physics,
    base_objects,
    mgl,
    smath,
    signal,
    statesystem,
)

from soragl.ui import ui

# -------------------------------------------------------------- #
# setup

WW = 1280
WINDOW_SIZE = [WW, int(WW / 16 * 9)]
WW = 1280 // 2.3
FB_SIZE = [WW, int(WW / 16 * 9)]

# mac version -- since no opengl

# ------------------------------ #
# setup

SORA.initialize(
    {
        "fps": 30,
        "window_size": [1280, 720],
        "window_flags": pygame.RESIZABLE
        | pygame.DOUBLEBUF
        | pygame.HWSURFACE
        | pygame.OPENGL
        if SORA.get_os() == SORA.OS_WINDOWS
        else 0,
        "window_bits": 32,
        "framebuffer_flags": pygame.SRCALPHA,
        "framebuffer_size": FB_SIZE,
        "framebuffer_bits": 32,
        "debug": False,
    }
)

SORA.create_context()

# if moderngl stuff setup
if SORA.is_flag_active(pygame.OPENGL):
    mgl.ModernGL.create_context(
        options={
            "standalone": False,
            "gc_mode": "context_gc",
            "clear_color": [0.0, 0.0, 0.0, 1.0],
        }
    )

# -------------------------------------------------------------- #
# imports

from scripts import singleton

from scripts import boid, explode


# -------------------------------------------------------------- #

sc = scene.Scene(config=scene.load_config(scene.Scene.DEFAULT_CONFIG))
sc._config["chunkpixw"] = SORA.FSIZE[0] // singleton.CHUNKS
sc._config["chunkpixh"] = SORA.FSIZE[1] // singleton.CHUNKS
sc._config["render_distance"] = singleton.CHUNKS + 2

scw = sc.make_layer(
    sc.get_config(),
    1,
    [
        base_objects.TileMapDebug(),
        base_objects.SpriteRendererAspect(),
        base_objects.Collision2DAspect(),
        # base_objects.Collision2DRendererAspectDebug(),
        # base_objects.Area2DAspect(),
        base_objects.Area2DRendererAspectDebug(),
        base_objects.ScriptAspect(),
        base_objects.CameraAspect(),
    ],
)


print(SORA.FSIZE)

for i in range(200):
    scw.add_entity(boid.Boid(random.randint(0, 200), random.randint(0, 200)))

# test1 = scw.add_entity(boid.Boid(100, 100))


# -------------------------------- #

BG_COL = (0, 0, 0)

# -------------------------------- #
# add to scw -- game world

# -- add entities
# particle handler test
# ph = scw.add_entity(physics.ParticleHandler(handler_type="square"))
# ph.position += (100, 100)
# ph["interval"] = 1 / 15

# ph = scw.add_entity(physics.ParticleHandler(handler_type="triangle"))
# ph.position += (200, 100)
# ph["interval"] = 1 / 15


# TODO - figure out how ot add signal s+ et

explode_signal = signal.register_signal(explode.ExplodeSignalRegister())
explode_receive = explode.ExplodeReceiver()
explode_signal.add_receiver(explode_receive)



# -------------------------------- #
# push scene
scene.SceneHandler.push_scene(sc)


# -------------------------------------------------------------- #
# game loop
SORA.start_engine_time()
while SORA.RUNNING:
    # SORA.FRAMEBUFFER.fill((255, 255, 255, 255))
    # SORA.FRAMEBUFFER.fill((0, 0, 0, 255))
    SORA.FRAMEBUFFER.fill(BG_COL)
    SORA.DEBUGBUFFER.fill((0, 0, 0, 0))
    # pygame update + render
    scene.SceneHandler.update()

    if SORA.is_key_clicked(pygame.K_d) and SORA.is_key_pressed(pygame.K_LSHIFT):
        SORA.DEBUG = not SORA.DEBUG
    if SORA.is_key_clicked(pygame.K_SPACE):
        explode_signal.emit_signal()

    # update signals
    signal.handle_signals()
    # push frame
    SORA.push_framebuffer()
    # pygame.display.flip()
    # update events
    SORA.update_hardware()
    SORA.handle_pygame_events()
    # clock tick
    SORA.CLOCK.tick(SORA.FPS)
    SORA.update_time()

# ------------------------------- #

pygame.quit()
