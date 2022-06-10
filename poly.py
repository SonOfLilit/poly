import pyglet
import math


def clamp(x, smallest, largest):
    return max(smallest, min(x, largest))


pyglet.resource.path = ["assets"]
pyglet.resource.reindex()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


images = {k: pyglet.resource.image(k + ".png") for k in ["unit", "bullet", "turret"]}

for image in images.values():
    center_image(image)

main_batch = pyglet.graphics.Batch()


class UnitAI:
    def __init__(self, unit) -> None:
        self.unit = unit
        self.unit.set_speed(1)

    def update(self, dt):
        self.unit.left(0.5 * dt)


class Unit(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch):
        self.velocity = 0.0
        self.ai = UnitAI(self)

        super().__init__(img=images["unit"], x=x, y=y, batch=batch, subpixel=True)

    def _update_rotation(self, dr):
        self.rotation += dr
        r = -math.radians(self.rotation)
        self.orientation = (math.sin(r), math.cos(r))

    def right(self, dt):
        self._update_rotation(-10 * dt)

    def left(self, dt):
        self._update_rotation(10 * dt)

    def set_speed(self, speed):
        self.velocity = 20.0 * clamp(speed, -0.5, 1.0)

    def update(self, dt):
        if not hasattr(self, "orientation"):
            self._update_rotation(0.0)
        x_part, y_part = self.orientation
        self.x -= x_part * self.velocity * dt
        self.y += y_part * self.velocity * dt


def update(dt):
    for obj in units:
        obj.update(dt)


def update_ai(dt):
    for obj in units:
        obj.ai.update(dt)


units = [Unit(x=100 + 100 * i, y=100, batch=main_batch) for i in range(4)]

turrets = [
    pyglet.sprite.Sprite(img=images["turret"], x=100 + 200 * i, y=600, batch=main_batch)
    for i in range(3)
]

window = pyglet.window.Window(1024, 768)
pyglet.gl.glClearColor(1, 1, 1, 1)
pyglet.clock.schedule_interval(update, 1 / 120.0)
pyglet.clock.schedule_interval(update_ai, 1 / 30.0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    print((x, y))


@window.event
def on_draw():
    window.clear()
    main_batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
