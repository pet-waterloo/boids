import pygame
import soragl as SORA
import struct

from pygame import draw as pgdraw
from pygame import math as pgmath
from soragl import animation, scene, physics, base_objects, mgl

# ------------------------------ #
# setup
SORA.initialize(
    {
        "fps": 30,
        "window_size": [1280, 720],
        "window_flags": pygame.RESIZABLE, #| pygame.OPENGL | pygame.DOUBLEBUF,
        "window_bits": 32,
        "framebuffer_flags": pygame.SRCALPHA,
        "framebuffer_size": [1280 // 3, 720 // 3],
        "framebuffer_bits": 32,
        "debug": True,
    }
)

SORA.create_context()

# ------------------------------ #
# import gl?
if SORA.is_flag_active(pygame.OPENGL):
    from soragl import mgl
    from soragl.mgl import ModernGL
    print("Configured Pygame for OpenGL")


# ------------------------------ #



sc = scene.Scene(config=scene.load_config(scene.Scene.DEFAULT_CONFIG))
scw = sc.make_layer(sc.get_config(), 1)
scw.get_chunk(0, 0)

# sce = physics.Entity()
# sceparticle = physics.ParticleHandler(create_func="custom", update_func="custom")
# sceparticle.position += (200, 150)
# sceparticle["interval"] = 0.5

# # add entities to world first
# scw.add_entity(sce)
# scw.add_entity(sceparticle)

# # entity comp
# sce.add_component(base_objects.Collision2DComponent())
# sce.position += (100, 100)
# sce.area = (20, 20)
# # sce1.static = True

# # physics
# sce.add_component(base_objects.Collision2DComponent())




# aspects
scw.add_aspect(base_objects.TileMapDebug())
scw.add_aspect(base_objects.Collision2DRendererAspectDebug())

# push scene
scene.SceneHandler.push_scene(sc)

# ------------------------------ #
# game loop
SORA.start_engine_time()
while SORA.RUNNING:
    # SORA.FRAMEBUFFER.fill((255, 255, 255, 255))
    SORA.FRAMEBUFFER.fill((0, 0, 0, 255))
    SORA.DEBUGBUFFER.fill((0, 0, 0, 0))
    # pygame update + render
    scene.SceneHandler.update()

    if SORA.is_key_clicked(pygame.K_d) and SORA.is_key_pressed(pygame.K_LSHIFT):
        SORA.DEBUG = not SORA.DEBUG

    SORA.FRAMEBUFFER.blit(SORA.DEBUGBUFFER, (0, 0))

    # push frame
    # SORA.push_framebuffer()
    pygame.display.flip()
    # update events
    SORA.update_hardware()
    SORA.handle_pygame_events()
    # clock tick
    SORA.CLOCK.tick(SORA.FPS)
    SORA.update_time()

pygame.quit()
