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

        self.possible_chunks = {
            name: colliders
            for name, colliders
            in source.CHUNKS.items()
            if name != "start"
        }

        self.chunks = {}
        chunk = source.Chunk(0, self.physics_space)
        chunk.create_sprite(self)
        self.last_chunk = "start"
        chunk_type = "start"
        self.chunks[0] = chunk

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
        self.resources["player"] = engine.load_animation(
            player_img, player_data)

        self.resources["chunks"] = {}
        for chunk_type in source.CHUNKS.keys():
            self.resources["chunks"][chunk_type] = pyglet.resource.image(
                f"resources/chunks/{chunk_type}.png")

    def update(self, dt):
        super().update(dt)
        self.player.update(dt)

        last_chunk_pos = list(self.chunks.keys())[
            len(self.chunks.keys())-1]*256
        if self.player.position.x+256*2 > last_chunk_pos:
            player_chunk = int(self.player.position.x // 256)
            last_chunk_pos_chunked = int(last_chunk_pos // 256)
            for x in range(last_chunk_pos_chunked+1, player_chunk+3):
                chunk_type = self.last_chunk
                while chunk_type == self.last_chunk:
                    chunk_type = random.choice(
                        list(self.possible_chunks.keys()))
                chunk = source.Chunk(x, self.physics_space,
                                     chunk_type=chunk_type)
                chunk.create_sprite(self)
                self.chunks[x] = chunk
                self.last_chunk = chunk_type

        if self.player.position.y < -128:
            self.player.state = "dead"

        self.position_camera(
            position=self.player.position, zoom=2,
            min_pos=(64, 0)
        )


if __name__ == "__main__":
    application = Application()
    application.run()
