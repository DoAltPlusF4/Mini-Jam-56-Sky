import pymunk

import engine


class Floor(engine.Entity):
    def __init__(self, x, y, space):
        super().__init__(
            position=(x*256, y-256),
            body_type=pymunk.Body.STATIC,
            collider={
                "type": "rect",
                "x": 0, "y": 0,
                "width": 254,
                "height": 254,
                "radius": 1,
                "collision_type": 0
            }
        )
        self.space = space
        self.colliders[0].friction = 0.5
    
    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["floor"], 
            (-128, -102), 
            batch=self.application.world_batch,
            group=self.application.world_layers["floor"]
        )
