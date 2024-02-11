import pyglet
from pyglet import shapes
def on_button_press():
    print("Hello")

window = pyglet.window.Window()

button_label = pyglet.text.Label('Press SPACE to say Hello',
                                font_name='Arial',
                                font_size=36,
                                x=window.width//2, y=window.height//2,
                                anchor_x='center', anchor_y='center')

batch = pyglet.graphics.Batch()
square = shapes.Rectangle(window.width//2 - 50, window.height//2 - 50, 100, 100, batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    button_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(symbol)
    if symbol == pyglet.window.key.SPACE:
        on_button_press()

pyglet.app.run()