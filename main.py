import json
import random

import pyglet
import pymunk

import engine
import source


class Application(engine.Application):
    def __init__(self):
        self.load_resources()

        super().__init__(
            caption="Doughnut Guy",
            default_size=(800, 550),
            minimum_size=(300, 170),
            fps_counter=True,
            world_layers=["player", "floor"],
            ui_layers=[]
        )
        self._debug_mode = True
        pyglet.gl.glClearColor(0.25, 0.5, 1, 1)

        self.physics_space.gravity = (0, -100)
        self.physics_space.damping = 0.5

        self.floor = []
        for x in range(-2, 3):
            floor = source.Floor(x, random.randint(0, 1), self.physics_space)
            floor.create_sprite(self)
            self.floor.append(floor)

        self.player = source.Player(self.physics_space)
        self.window.push_handlers(self.player)
        self.player.create_sprite(self)
    
    def load_resources(self):
        self.resources = {}

        pyglet.resource.add_font("resources/fonts/m5x7.ttf")
        self.resources["font"] = pyglet.font.load(name="m5x7")

        player_img = pyglet.resource.image("resources/sprites/player.png")
        with open("resources/sprites/player.json", "r") as f:
            player_data = json.load(f)
        self.resources["player"] = engine.load_animation(player_img, player_data)

        self.resources["floor"] = pyglet.resource.image("resources/sprites/floor.png")
    
    def update(self, dt):
        super().update(dt)
        self.player.update(dt)
        self.position_camera(
            position=self.player.position, zoom=2,
            min_pos=(None, -50)
        )


if __name__ == "__main__":
    application = Application()
    application.run()
