import pyglet

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

units = [
    pyglet.sprite.Sprite(img=images["unit"], x=100 + 100 * i, y=100, batch=main_batch)
    for i in range(4)
]

turrets = [
    pyglet.sprite.Sprite(img=images["turret"], x=100 + 200 * i, y=500, batch=main_batch)
    for i in range(3)
]

game_window = pyglet.window.Window(800, 600)
pyglet.gl.glClearColor(1, 1, 1, 1)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
