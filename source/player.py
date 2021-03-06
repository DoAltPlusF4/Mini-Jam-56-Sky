import engine
from engine import key
import pyglet

SPEED = 150
JUMP_VELOCITY = 90


class Player(engine.Entity):
    _state = "idle"

    def __init__(self, space):
        super().__init__(
            colliders=[
                {
                    "type": "rect",
                    "x": 0, "y": -2,
                    "width": 12,
                    "height": 24,
                    "radius": 2,
                    "collision_type": 0
                }
            ]
        )
        self.space = space

        self.controls = {
            "left": False,
            "right": False,
            "jump": False
        }

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self.state:
            self._state = state
            self.sprite.image = self.application.resources["player"][state]
            if state == "dead":
                if self.application.score > self.application.hi_score:
                    self.application.hi_score = self.application.score
                    self.application.high_score_text.text = "New Hi-Score!"
                self.application.show_death_screen()
                self.application.sounds["dead"].play()

    def update(self, dt):
        if self.state != "dead":
            self.controls["left"] = self.application.key_handler[key.A]
            self.controls["right"] = self.application.key_handler[key.D]

            if self.controls["jump"]:
                self.controls["jump"] -= dt
                if self.controls["jump"] < 0:
                    self.controls["jump"] = False
            if self.application.key_handler[key.SPACE] or self.application.key_handler[key.W]:
                self.controls["jump"] = 0.02

            if self.controls["jump"] and round(self.velocity.y) == 0 and self.state != "jumping":
                self.controls["jump"] = False
                self.apply_impulse_at_local_point((0, JUMP_VELOCITY))
                self.state = "jumping"
                self.application.sounds["jump"].play()

            if self.state == "jumping":
                if self.velocity.y < 0:
                    self.state = "idle"

                if self.application.key_handler[key.SPACE] or self.application.key_handler[key.W]:
                    pass
                else:
                    self.apply_force_at_local_point((0, -500), (0, 0))

            if self.controls["left"] and not self.controls["right"]:
                self.flip = True
            if not self.controls["left"] and self.controls["right"]:
                self.flip = False

            vx = 0
            if self.controls["left"]:
                vx -= SPEED
            if self.controls["right"]:
                vx += SPEED

            if round(self.velocity.y) == 0:
                if vx != 0:
                    if self.state != "jumping":
                        self.state = "walk"
                    self.colliders[0].friction = 1
                else:
                    if self.state != "jumping":
                        self.state = "idle"
                    self.colliders[0].friction = 15
            else:
                self.colliders[0].friction = 1

            if self.velocity.x > 0 and self.controls["left"]:
                self.colliders[0].friction = 15
            elif self.velocity.x < 0 and self.controls["right"]:
                self.colliders[0].friction = 15
            self.velocity = (
                max(min(self.velocity.x, SPEED/2), -SPEED/2), self.velocity.y)

            self.apply_force_at_local_point((vx, 0), (0, 0))

        self.update_sprite()

    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["player"]["idle"],
            (-16, -16),
            batch=self.application.world_batch,
            group=self.application.world_layers["player"]
        )
