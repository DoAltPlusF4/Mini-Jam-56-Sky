import engine


class WaterDrop(engine.Entity):
    _state = "falling"

    def __init__(self, space, x, y):
        super().__init__(
            position=(x, y),
            mass=3,
            collider={
                "type": "circle",
                "offset": (0, -5),
                "radius": 8,
                "collision_type": 4
            }
        )
        self.space = space
        self.done = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self.state:
            self._state = state
            self.sprite.image = self.application.resources["water_drop"][state]

    def update(self, dt):
        self.update_sprite()

    def on_animation_end(self):
        p_x = self.application.player.position.x
        if self.state == "hit":
            self.delete()
            self.done = True

    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["water_drop"]["falling"],
            (-16, -16),
            batch=self.application.world_batch,
            group=self.application.world_layers["tap_balloon"]
        )
        self.sprite.push_handlers(self)
