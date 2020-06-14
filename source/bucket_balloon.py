import random

import pyglet
import pymunk

import engine
import source
from engine import key


class BucketBalloon(engine.Entity):
    _state = "idle"

    def __init__(self, space, x, y):
        super().__init__(
            position=(x, y),
            body_type=pymunk.Body.DYNAMIC
        )
        self.space = space

        def position_func(space, dt):
            distance_y = self.application.player.position.y - self.position.y + 140
            self.position = (
                self.position.x,
                self.position.y+distance_y*dt
            )
        self.position_func = position_func
        self.timer = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self.state:
            self._state = state
            self.sprite.image = self.application.resources["balloon"][state]
            if state == "throw_water":
                self.timer = 0.5

    def update(self, dt):
        self.update_sprite()
        if self.timer is not None:
            self.timer -= dt
            if self.timer < 0:
                self.timer = None
                water_drop = source.WaterDrop(
                    self.space, self.position.x+16, self.position.y-40)
                water_drop.create_sprite(self.application)
                self.application.water_drops.append(water_drop)
        p_x = self.application.player.position.x
        if self.state == "idle":
            if self.position.x-64 < p_x < self.position.x+64:
                self.state = "throw_water"

    def on_animation_end(self):
        if self.state == "throw_water":
            self.state = "refill"
        elif self.state == "refill":
            self.state = "idle"

    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["balloon"]["idle"],
            (-80/2, -112/2),
            batch=self.application.world_batch,
            group=self.application.world_layers["bucket_balloon"]
        )
        self.sprite.push_handlers(self)
