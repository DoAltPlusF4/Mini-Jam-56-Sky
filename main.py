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
        pyglet.gl.glClearColor(0.25, 0.5, 1, 1)

        self.physics_space.gravity = (0, -100)

        player_to_water = self.physics_space.add_collision_handler(0, 2)
        def begin(arbiter, space, data):
            self.player.state = "dead"
            return False
        player_to_water.begin = begin

        self.chunks = {}
        chunk = source.Chunk(0, self.physics_space)
        chunk.create_sprite(self)
        self.chunks[0] = chunk

        possible_chunks = {name: colliders for name, colliders in source.CHUNKS.items() if name != "start"}
        for x in range(1, 5):
            chunk_type = random.choice(list(possible_chunks.keys()))
            chunk = source.Chunk(x, self.physics_space, chunk_type=chunk_type)
            chunk.create_sprite(self)
            self.chunks[x] = chunk

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

        self.resources["chunks"] = {}
        for chunk_type in source.CHUNKS.keys():
            self.resources["chunks"][chunk_type] = pyglet.resource.image(f"resources/chunks/{chunk_type}.png")
    
    def update(self, dt):
        super().update(dt)
        self.player.update(dt)
        if self.player.position.y < -128:
            self.player.state = "dead"
        self.position_camera(
            position=self.player.position, zoom=2,
            min_pos=(64, 32)
        )


if __name__ == "__main__":
    application = Application()
    application.run()
