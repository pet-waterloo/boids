

import soragl as SORA

from soragl import signal, scene

from scripts import boid


class ExplodeSignal(signal.SignalRegister):
    def __init__(self):
        super().__init__("explode")

    def emit(self, args: dict):
        self._emit_signal(args)
    

class ExplodeReceiver(signal.Receiver):
    def __init__(self):
        super().__init__(self._explode_boids)

    def call(self, args: dict):
        if not self.active: return
        self._call(args)

    def explode_boids(self, args: dict):
        # dict is empty
        # go through every single boid + set random velocity vector
        for layer in scene.SceneHandler.CURRENT._layers:
            for e in layer.iter_active_entities_filter_type(boid.Boid):
                # reset velocity
                e.velocity = SORA.smath.normalized_random_vec2() * (
                    (SORA.random.random() - 0.5) * 40 + 80
                )


