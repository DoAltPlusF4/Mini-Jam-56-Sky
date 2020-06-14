import pyglet


class Button(pyglet.event.EventDispatcher):
    def __init__(self, x, y, in_img, out_img, hover_img, batch=None, group=None):
        self._x = x
        self._y = y
        self._width = out_img.width
        self._height = out_img.height
        self._in_img = in_img
        self._out_img = out_img
        self._hover_img = hover_img
        self._sprite = pyglet.sprite.Sprite(
            out_img, x, y, batch=batch, group=group)
        self._pressed = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._sprite.x = x

    @property
    def y(self):
        return self._x

    @y.setter
    def y(self, y):
        self._y = y
        self._sprite.y = y

    @property
    def scale(self):
        return self._sprite.scale

    @scale.setter
    def scale(self, scale):
        self._sprite.scale = scale

    @property
    def visible(self):
        return self._sprite.visible

    @visible.setter
    def visible(self, visible):
        self._sprite.visible = visible

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width*self.scale and self._y < y < self._y + self._height*self.scale

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._check_hit(x, y):
            return
        self._sprite.image = self._in_img
        self._pressed = True
        self.dispatch_event('on_press')
        self.on_press()

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._sprite.image = self._out_img
        self._pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self._pressed:
            return
        if self._check_hit(x, y):
            self._sprite.image = self._hover_img
        else:
            self._sprite.image = self._out_img

    def on_press(self):
        pass


Button.register_event_type('on_press')
