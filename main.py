import json
import random

import pyglet
import pymunk

import engine
import source


class Application(engine.Application):
    def __init__(self):
        self.state = "main_menu"
        self.score = 0
        self.load_resources()

        super().__init__(
            caption="Run, Doughnut, Run!",
            default_size=(800, 550),
            minimum_size=(300, 170),
            fps_counter=False,
            world_layers=[
                "player",
                "floor",
                "player_dead",
                "bucket_balloon",
                "tap_balloon",
                "clouds"
            ],
            ui_layers=[
                "bg",
                "logo",
                "buttons",
                "score",
                "text"
            ]
        )
        pyglet.gl.glClearColor(0.25, 0.5, 1, 1)

        self.physics_space.gravity = (0, -100)

        player_to_water = self.physics_space.add_collision_handler(0, 2)

        def begin(arbiter, space, data):
            self.player.state = "dead"
            self.player.sprite.group = self.world_layers["player_dead"]
            self.player.sprite.opacity = 96
            return False
        player_to_water.begin = begin

        player_to_water_other = self.physics_space.add_collision_handler(0, 3)

        def begin(arbiter, space, data):
            self.player.state = "dead"
            return False
        player_to_water_other.begin = begin

        water_drop_c = self.physics_space.add_wildcard_collision_handler(4)

        def begin(arbiter, space, data):
            if arbiter.shapes[1].collision_type == 0:
                self.player.state = "dead"
                arbiter.shapes[0].body.state = "hit"
                arbiter.shapes[0].body.space = None
                return False
            elif arbiter.shapes[1].collision_type != 3:
                arbiter.shapes[0].body.state = "hit"
                arbiter.shapes[0].body.space = None
                self.sounds["water_drop"].play()
                return True
            else:
                return False
        water_drop_c.begin = begin

        self.water_drops = []

        self.chunks = {}
        self.possible_chunks = {
            name: colliders
            for name, colliders
            in source.CHUNKS.items()
            if name != "start"
        }

        self.score_text = pyglet.text.Label(
            "Score: 0", font_name="m5x7", font_size=64,
            color=(25, 25, 100, 255),
            anchor_x="right",
            anchor_y="top",
            batch=self.ui_batch,
            group=self.ui_layers["score"]
        )

        # Main Menu UI
        self.menu_bg = pyglet.sprite.Sprite(
            self.resources["menu_bg"],
            0, 0,
            batch=self.ui_batch,
            group=self.ui_layers["bg"]
        )
        self.logo = pyglet.sprite.Sprite(
            self.resources["logo"],
            0, 0,
            batch=self.ui_batch,
            group=self.ui_layers["logo"]
        )
        self.start_button = source.Button(
            0, 0, *self.resources["start_button"],
            batch=self.ui_batch, group=self.ui_layers["buttons"]
        )
        self.close_button = source.Button(
            0, 0, *self.resources["close_button"],
            batch=self.ui_batch, group=self.ui_layers["buttons"]
        )
        self.reset_score_button = source.Button(
            0, 0, *self.resources["reset_score_button"],
            batch=self.ui_batch, group=self.ui_layers["buttons"]
        )

        def on_start_press():
            self.hide_menu()
            self.setup_game()
        self.start_button.on_press = on_start_press

        def on_close_press():
            self.window.close()
        self.close_button.on_press = on_close_press

        def reset_score_press():
            self.hi_score = 0
            self.score_text.text = f"Hi-Score: {self.hi_score}"
        self.reset_score_button.on_press = reset_score_press

        self.show_menu()

        # Death UI
        self.death_panel = pyglet.shapes.Rectangle(
            0, 0, 100, 100,
            batch=self.ui_batch,
            group=self.ui_layers["bg"]
        )
        self.death_panel.opacity = 128
        self.death_score = pyglet.text.Label(
            "", font_name="m5x7", font_size=64,
            color=(25, 25, 50, 255),
            anchor_x="center",
            anchor_y="center",
            batch=self.ui_batch,
            group=self.ui_layers["text"]
        )
        self.death_text = pyglet.text.Label(
            "You Died!", font_name="m5x7",
            font_size=64,
            color=(100, 25, 25, 255),
            anchor_x="center",
            anchor_y="center",
            batch=self.ui_batch,
            group=self.ui_layers["text"]
        )
        self.high_score_text = pyglet.text.Label(
            "", font_name="m5x7",
            font_size=64,
            color=(255, 255, 25, 255),
            anchor_x="center",
            anchor_y="center",
            batch=self.ui_batch,
            group=self.ui_layers["text"]
        )

        self.menu_button = source.Button(
            0, 0, *self.resources["menu_button"],
            batch=self.ui_batch, group=self.ui_layers["buttons"]
        )
        self.restart_button = source.Button(
            0, 0, *self.resources["restart_button"],
            batch=self.ui_batch, group=self.ui_layers["buttons"]
        )

        def on_menu_press():
            self.hide_death_screen()
            self.show_menu()
            self.state = "main_menu"
            for drop in self.water_drops:
                try:
                    drop.delete()
                except:
                    pass
            self.water_drops = []
            for i in list(self.chunks.keys()):
                chunk = self.chunks[i]
                chunk.delete()
                del self.chunks[i]
                del chunk
            if hasattr(self, "player"):
                self.player.delete()
                del self.player
            if hasattr(self, "tap_balloon"):
                self.tap_balloon.delete()
                del self.tap_balloon

        self.menu_button.on_press = on_menu_press

        def on_restart_press():
            self.hide_death_screen()
            self.setup_game()

        self.restart_button.on_press = on_restart_press

        self.hide_death_screen()

        self.on_resize(self.window.width, self.window.height)

    @property
    def hi_score(self):
        with open("data/data.json", "r") as f:
            return json.load(f)["hi_score"]

    @hi_score.setter
    def hi_score(self, hi_score):
        with open("data/data.json", "w") as f:
            return json.dump({"hi_score": hi_score}, f)

    def show_death_screen(self):
        self.death_panel.visible = True
        self.death_text.text = "You Died!"
        self.death_score.text = f"Your Score: {self.score}"
        self.restart_button.visible = True
        self.menu_button.visible = True
        self.window.push_handlers(self.restart_button)
        self.window.push_handlers(self.menu_button)
        self.music.pause()

    def hide_death_screen(self):
        self.death_panel.visible = False
        self.death_text.text = ""
        self.death_score.text = ""
        self.high_score_text.text = ""
        self.restart_button.visible = False
        self.menu_button.visible = False
        self.restart_button.on_mouse_release(0, 0, 0, 0)
        self.window.remove_handlers(self.restart_button)
        self.menu_button.on_mouse_release(0, 0, 0, 0)
        self.window.remove_handlers(self.menu_button)
        self.music.play()

    def show_menu(self):
        self.logo.visible = True
        self.menu_bg.visible = True
        self.start_button.visible = True
        self.close_button.visible = True
        self.reset_score_button.visible = True
        self.window.push_handlers(self.start_button)
        self.window.push_handlers(self.close_button)
        self.window.push_handlers(self.reset_score_button)
        self.score_text.text = f"Hi-Score: {self.hi_score}"

    def hide_menu(self):
        self.logo.visible = False
        self.menu_bg.visible = False
        self.start_button.visible = False
        self.close_button.visible = False
        self.reset_score_button.visible = False
        self.start_button.on_mouse_release(0, 0, 0, 0)
        self.window.remove_handlers(self.start_button)
        self.close_button.on_mouse_release(0, 0, 0, 0)
        self.window.remove_handlers(self.close_button)
        self.reset_score_button.on_mouse_release(0, 0, 0, 0)
        self.window.remove_handlers(self.reset_score_button)

    def on_resize(self, width, height):
        scale = min(
            self.window.width/self.default_size[0],
            self.window.height/self.default_size[1]
        ) / 2

        self.logo.scale = scale
        self.menu_bg.scale = scale
        self.start_button.scale = scale*3
        self.close_button.scale = scale*3
        self.reset_score_button.scale = scale*3

        self.score_text.font_size = scale*64
        self.score_text.x = width
        self.score_text.y = height

        self.logo.x = width//2 - self.logo.width//2
        self.logo.y = height - self.logo.height - 50*scale

        self.menu_bg.x = width//2 - self.menu_bg.width//2
        self.menu_bg.y = height//2 - self.menu_bg.height//2

        self.start_button.x = width//2 - self.start_button._sprite.width//2
        self.start_button.y = height//2 - self.start_button._sprite.height//2 + 50*scale

        self.close_button.x = width//2 - self.close_button._sprite.width//2
        self.close_button.y = height//2 - self.close_button._sprite.height//2 - 50*scale

        self.reset_score_button.x = width - self.close_button._sprite.width
        self.reset_score_button.y = 0

        self.death_panel.width = scale*1000
        self.death_panel.height = scale*600
        self.menu_button.scale = scale*4
        self.restart_button.scale = scale*4

        self.death_score.font_size = scale*128
        self.death_score.x = width//2
        self.death_score.y = height//2

        self.death_text.font_size = scale*192
        self.death_text.x = width//2
        self.death_text.y = height//2 + 200*scale

        self.high_score_text.font_size = scale*64
        self.high_score_text.x = width//2
        self.high_score_text.y = height//2 - 80*scale

        self.menu_button.x = width//2 - self.menu_button._sprite.width//2 + 150*scale
        self.menu_button.y = height//2 - self.menu_button._sprite.height//2 - 200*scale

        self.restart_button.x = width//2 - self.restart_button._sprite.width//2 - 150*scale
        self.restart_button.y = height//2 - \
            self.restart_button._sprite.height//2 - 200*scale

        self.death_panel.x = width//2 - self.death_panel.width//2
        self.death_panel.y = height//2 - self.death_panel.height//2

    def setup_game(self):
        for drop in self.water_drops:
            try:
                drop.delete()
            except:
                pass
        self.water_drops = []
        for i in list(self.chunks.keys()):
            chunk = self.chunks[i]
            chunk.delete()
            del self.chunks[i]
            del chunk
        if hasattr(self, "player"):
            self.player.delete()
            del self.player
        if hasattr(self, "tap_balloon"):
            self.tap_balloon.delete()
            del self.tap_balloon

        self.player = source.Player(self.physics_space)
        self.player.create_sprite(self)

        self.tap_balloon = source.TapBalloon(self.physics_space)
        self.tap_balloon.create_sprite(self)

        chunk = source.Chunk(0, self.physics_space)
        chunk.create_sprite(self)
        self.last_chunk = "start"
        chunk_type = "start"
        self.chunks[0] = chunk

        self.state = "in_game"

    def load_resources(self):
        self.resources = {}

        pyglet.resource.add_font("resources/fonts/m5x7.ttf")
        self.resources["font"] = pyglet.font.load(name="m5x7")

        player_img = pyglet.resource.image("resources/sprites/player.png")
        with open("resources/sprites/player.json", "r") as f:
            player_data = json.load(f)
        self.resources["player"] = engine.load_animation(
            player_img, player_data)

        balloon_img = pyglet.resource.image("resources/sprites/balloon.png")
        with open("resources/sprites/balloon.json", "r") as f:
            balloon_data = json.load(f)
        self.resources["balloon"] = engine.load_animation(
            balloon_img, balloon_data)

        tap_balloon_img = pyglet.resource.image(
            "resources/sprites/tap_balloon.png")
        with open("resources/sprites/tap_balloon.json", "r") as f:
            tap_balloon_data = json.load(f)
        self.resources["tap_balloon"] = engine.load_animation(
            tap_balloon_img, tap_balloon_data)["idle"]

        water_drop_img = pyglet.resource.image(
            "resources/sprites/water_drop.png")
        with open("resources/sprites/water_drop.json", "r") as f:
            water_drop_data = json.load(f)
        self.resources["water_drop"] = engine.load_animation(
            water_drop_img, water_drop_data)

        cloud_img = pyglet.resource.image("resources/sprites/cloud.png")
        cloud_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(cloud_img, 1, 3)
        )
        self.resources["clouds"] = cloud_grid

        self.resources["chunks"] = {}
        for chunk_type in source.CHUNKS.keys():
            self.resources["chunks"][chunk_type] = pyglet.resource.image(
                f"resources/chunks/{chunk_type}.png")

        logo_img = pyglet.resource.image("resources/sprites/logo.png")
        self.resources["logo"] = logo_img

        bg_img = pyglet.resource.image("resources/sprites/menu_bg.png")
        self.resources["menu_bg"] = bg_img

        start_button_img = pyglet.resource.image(
            "resources/sprites/start_button.png")
        start_button_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(start_button_img, 1, 3)
        )
        self.resources["start_button"] = start_button_grid

        close_button_img = pyglet.resource.image(
            "resources/sprites/close_button.png")
        close_button_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(close_button_img, 1, 3)
        )
        self.resources["close_button"] = close_button_grid

        reset_score_button_img = pyglet.resource.image(
            "resources/sprites/reset_score_button.png")
        reset_score_button_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(reset_score_button_img, 1, 3)
        )
        self.resources["reset_score_button"] = reset_score_button_grid

        menu_button_img = pyglet.resource.image(
            "resources/sprites/menu_button.png")
        menu_button_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(menu_button_img, 1, 3)
        )
        self.resources["menu_button"] = menu_button_grid

        restart_button_img = pyglet.resource.image(
            "resources/sprites/restart_button.png")
        restart_button_grid = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(restart_button_img, 1, 3)
        )
        self.resources["restart_button"] = restart_button_grid

        self.sounds = {}
        self.sounds["jump"] = pyglet.media.load(
            "resources/sounds/jump.wav", streaming=False)
        self.sounds["water_drop"] = pyglet.media.load(
            "resources/sounds/water_drop.wav", streaming=False)
        self.sounds["in_game"] = pyglet.media.load(
            "resources/sounds/in_game.wav", streaming=False)
        self.sounds["dead"] = pyglet.media.load(
            "resources/sounds/dead.wav", streaming=False)
        self.music = pyglet.media.Player()
        self.music.queue(self.sounds["in_game"])
        self.music.play()
        self.music.loop = True

    def update(self, dt):
        if self.state == "in_game":
            super().update(dt)
            self.player.update(dt)
            self.tap_balloon.update(dt)

            for chunk in self.chunks.values():
                chunk.update(dt)

            for drop in self.water_drops:
                if not drop.done:
                    drop.update(dt)
                else:
                    self.water_drops.remove(drop)

            tap_boi_chunk = int((self.tap_balloon.position.x-128) // 256)

            try:
                last_chunk_pos = list(self.chunks.keys())[
                    len(self.chunks.keys())-1]*256
                player_chunk = int((self.player.position.x-128) // 256)
                self.score = player_chunk+1
                self.score_text.text = f"Score: {self.score}"
                if self.player.position.x+256*2 > last_chunk_pos:
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

                x = list(self.chunks.keys())[0]
                if tap_boi_chunk-1 >= x:
                    self.chunks[x].delete()
                    del self.chunks[x]
            except IndexError:
                pass

            if self.player.position.y < -128:
                self.player.state = "dead"

            self.position_camera(
                position=self.player.position, zoom=2,
                min_pos=(64, 0)
            )


if __name__ == "__main__":
    application = Application()
    application.run()
