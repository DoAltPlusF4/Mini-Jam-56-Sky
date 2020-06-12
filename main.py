import json

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
            world_layers=["bg", "player"],
            ui_layers=[]
        )
        self._debug_mode = True
        pyglet.gl.glClearColor(0.25, 0.5, 1, 1)

        self.physics_space.gravity = (0, -100)
        self.physics_space.damping = 0.5

        self.floor = engine.Entity(
            position=(0, -50),
            body_type=pymunk.Body.STATIC,
            collider={
                "type": "rect",
                "x": 0, "y": 0,
                "width": 200,
                "height": 25,
                "radius": 0,
                "collision_type": 0
            }
        )
        self.floor.space = self.physics_space
        self.floor.colliders[0].friction = 0.5
        self.floor.create_sprite(self.resources["floor"], (-100, -12.5), batch=self.world_batch)

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
        self.position_camera(position=self.player.position, zoom=2)


if __name__ == "__main__":
    application = Application()
    application.run()
