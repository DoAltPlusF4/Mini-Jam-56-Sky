import pymunk

import engine


CHUNKS = {
    "start": [
        {
            "type": "rect",
            "x": 0, "y": -70,
            "width": 256,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -120, "y": 58,
            "width": 16,
            "height": 192,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "river1": [
        {
            "type": "rect",
            "x": -64, "y": -70,
            "width": 128,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 96, "y": -70,
            "width": 64,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 32, "y": -94,
            "width": 64,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 32, "y": -64,
            "width": 64,
            "height": 45,
            "radius": 0,
            "collision_type": 2
        },
        {
            "type": "rect",
            "x": 40, "y": 2,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -24, "y": -30,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "climb": [

    ],
    "river2": [
        
    ]
}



class Chunk(engine.Entity):
    def __init__(self, x, space, chunk_type="start"):
        self.type = chunk_type
        super().__init__(
            position=(x*256, 0),
            body_type=pymunk.Body.STATIC,
            colliders=CHUNKS[self.type]
        )
        self.space = space
        for col in self.colliders:
            col.friction = 0.5
    
    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["chunks"][self.type], 
            (-128, -102), 
            batch=self.application.world_batch,
            group=self.application.world_layers["floor"]
        )
