import pyglet
import pymunk

import engine
from engine import key


class TapBalloon(engine.Entity):
    def __init__(self, space):
        super().__init__(
            position=(-150, 0),
            body_type=pymunk.Body.DYNAMIC,
            collider={
                "type": "rect",
                "x": -15, "y": -49,
                "width": 7,
                "height": 398,
                "radius": 0,
                "collision_type": 3
            }
        )
        self.space = space

        def position_func(space, dt):
            distance_y = self.application.player.position.y - self.position.y - 64
            self.position = (
                self.position.x+32*dt,
                self.position.y+distance_y*dt
            )

        self.position_func = position_func

    def update(self, dt):
        self.update_sprite()

    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["tap_balloon"],
            (-80/2, -496/2),
            batch=self.application.world_batch,
            group=self.application.world_layers["tap_balloon"]
        )
