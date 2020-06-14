import random

import pyglet
import pymunk

import engine
import source

CHUNKS = {
    "start": [
        {
            "type": "rect",
            "x": 0, "y": -96,
            "width": 256,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -120, "y": 32,
            "width": 16,
            "height": 192,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "river1": [
        {
            "type": "rect",
            "x": -64, "y": -96,
            "width": 128,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 96, "y": -96,
            "width": 64,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 32, "y": -120,
            "width": 64,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 32, "y": -90,
            "width": 64,
            "height": 46,
            "radius": 0,
            "collision_type": 2
        },
        {
            "type": "rect",
            "x": 40, "y": -24,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -24, "y": -56,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "climb": [
        {
            "type": "rect",
            "x": -40, "y": -96,
            "width": 176,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -24, "y": -48,
            "width": 48,
            "height": 32,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -104, "y": -8,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -120, "y": 24,
            "width": 16,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -40, "y": 56,
            "width": 80,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 24, "y": 0,
            "width": 48,
            "height": 128,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 104, "y": 64,
            "width": 16,
            "height": 128,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 72, "y": -90,
            "width": 48,
            "height": 46,
            "radius": 0,
            "collision_type": 2
        },
        {
            "type": "rect",
            "x": 72, "y": -120,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 112, "y": -96,
            "width": 32,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "river2": [
        {
            "type": "rect",
            "x": -120, "y": -96,
            "width": 16,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -80, "y": -65,
            "width": 10,
            "height": 10,
            "radius": 3,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -64, "y": -63,
            "width": 6,
            "height": 6,
            "radius": 5,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -1, "y": -64,
            "width": 10,
            "height": 10,
            "radius": 3,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 15, "y": -65,
            "width": 10,
            "height": 10,
            "radius": 3,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 81, "y": -63,
            "width": 10,
            "height": 10,
            "radius": 3,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 120, "y": -96,
            "width": 16,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 0, "y": -120,
            "width": 224,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 0, "y": -90,
            "width": 224,
            "height": 45,
            "radius": 0,
            "collision_type": 2
        }
    ],
    "gap": [
        {
            "type": "rect",
            "x": -104, "y": -96,
            "width": 48,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -40, "y": -72,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 32, "y": -72,
            "width": 32,
            "height": 48,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 104, "y": -96,
            "width": 48,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "hop": [
        {
            "type": "rect",
            "x": -56, "y": -96,
            "width": 144,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -48, "y": -56,
            "width": 64,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": -16, "y": -24,
            "width": 32,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 48, "y": -112,
            "width": 64,
            "height": 32,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 104, "y": -96,
            "width": 48,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 48, "y": -81.5,
            "width": 64,
            "height": 29,
            "radius": 0,
            "collision_type": 2
        },
        {
            "type": "rect",
            "x": 48, "y": -8,
            "width": 32,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        }
    ],
    "river3": [
        {
            "type": "rect",
            "x": -120, "y": -96,
            "width": 16,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 0, "y": -120,
            "width": 224,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 120, "y": -96,
            "width": 16,
            "height": 64,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 0, "y": -89.5,
            "width": 224,
            "height": 45,
            "radius": 0,
            "collision_type": 2
        },
        {
            "type": "rect",
            "x": -56, "y": -72,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 56, "y": -72,
            "width": 48,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        },
        {
            "type": "rect",
            "x": 0, "y": -40,
            "width": 32,
            "height": 16,
            "radius": 0,
            "collision_type": 1
        }
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
        if chunk_type != "start":
            self.balloon = source.BucketBalloon(
                self.space, x*256+random.randint(-128, 128), 128
            )

    def update(self, dt):
        if hasattr(self, "balloon"):
            self.balloon.update(dt)

    def create_sprite(self, application):
        self.application = application
        super().create_sprite(
            self.application.resources["chunks"][self.type],
            (-128, -128),
            batch=self.application.world_batch,
            group=self.application.world_layers["floor"]
        )
        cloud_img = random.choice(self.application.resources["clouds"])
        self.cloud = pyglet.sprite.Sprite(
            cloud_img,
            self.position.x-180,
            self.position.y-202,
            batch=self.application.world_batch,
            group=self.application.world_layers["clouds"]
        )
        if hasattr(self, "balloon"):
            self.balloon.create_sprite(self.application)

    def delete(self):
        self.cloud.delete()
        if hasattr(self, "balloon"):
            self.balloon.delete()
        super().delete()
