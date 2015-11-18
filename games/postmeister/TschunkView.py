import sys
import pyglet
from pyglet.gl import *
import primitives
import utils
from map1 import *
import threading
import time

FPS = 60
smoothConfig = utils.getSmoothConfig()


class TschunkView(pyglet.window.Window):

    def mapX(self, x):
        return self.cord_origin_x + x * self.x_step

    def mapY(self, y):
        return self.cord_origin_y + y * self.y_step

    def __init__(self, mymap):
        super(
            TschunkView,
            self).__init__(
            fullscreen=False,
            caption='Tschunk!',
            config=smoothConfig)

        self.map = mymap

        self.image = pyglet.resource.image(mymap.img)
        self.sprite = pyglet.sprite.Sprite(self.image)

        self.y_step = self.image.height / mymap.rows + 1
        self.x_step = self.image.width / mymap.cols + 1
        self.cord_origin_x = self.x_step / 2
        self.cord_origin_y = self.y_step / 2

        self.x = mymap.origin_x
        self.y = mymap.origin_y
        start_x = self.mapX(self.x)
        start_y = self.mapY(self.y)

        self.direction = mymap.initial_direction

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        down  = pyglet.resource.image('games/postmeister/img/figure_down.png')
        self.img_down  = pyglet.sprite.Sprite(down)
        self.img_down.scale = float(self.y_step) / self.img_down.width
        self.img_down.image.anchor_x = self.img_down.image.width / 2
        self.img_down.image.anchor_y = self.img_down.image.height / 2

        up  = pyglet.resource.image('games/postmeister/img/figure_up.png')
        self.img_up  = pyglet.sprite.Sprite(up)
        self.img_up.scale = float(self.y_step) / self.img_up.width
        self.img_up.image.anchor_x = self.img_up.image.width / 2
        self.img_up.image.anchor_y = self.img_up.image.height / 2

        left  = pyglet.resource.image('games/postmeister/img/figure_left.png')
        self.img_left  = pyglet.sprite.Sprite(left)
        self.img_left.scale = float(self.y_step) / self.img_left.width
        self.img_left.image.anchor_x = self.img_left.image.width / 2
        self.img_left.image.anchor_y = self.img_left.image.height / 2

        right  = pyglet.resource.image('games/postmeister/img/figure_right.png')
        self.img_right  = pyglet.sprite.Sprite(right)
        self.img_right.scale = float(self.y_step) / self.img_right.width
        self.img_right.image.anchor_x = self.img_right.image.width / 2
        self.img_right.image.anchor_y = self.img_right.image.height / 2

        self.figures = dict()
        self.figures[90] = self.img_down
        self.figures[0] = self.img_right
        self.figures[270] = self.img_up
        self.figures[180] = self.img_left

        arrow  = pyglet.resource.image('games/postmeister/img/arrow.png')
        self.img_arrow  = pyglet.sprite.Sprite(arrow)
        self.img_arrow.scale = float(self.y_step) / self.img_arrow.width

        #rotate around the center:
        self.img_arrow.image.anchor_x = self.img_arrow.image.width / 2
        self.img_arrow.image.anchor_y = self.img_arrow.image.height / 2
        self.img_arrow.rotation = 90

        self.figure = self.figures[self.img_arrow.rotation]

        #self.l = primitives.Line((0,0),(100,100),stroke=10,color=(1,0,0,1))
        self.c = primitives.Circle(
            start_x, start_y, width=self.y_step, color=(
                1., 0., 0., 1.))
        self.drops = []

        # Setup debug framerate display:
        self.fps_display = pyglet.clock.ClockDisplay()

        # Schedule the update of this window, so it will advance in time at the
        # defined framerate.  If we don't, the window will only update on events
        # like mouse motion.

        #pyglet.clock.schedule_interval(self.update, 1.0)

        self.set_size(self.image.width, self.image.height)
        self.set_location(1000, 20)

    def on_draw(self):
        self.c.x = self.mapX(self.x)
        self.c.y = self.mapY(self.y)

        self.img_arrow.x = self.mapX(self.x)# - self.img_arrow.width/2
        self.img_arrow.y = self.mapY(self.y)# - self.img_arrow.height/2
        self.figure.x = self.mapX(self.x)# - self.img_arrow.width/2
        self.figure.y = self.mapY(self.y)# - self.img_arrow.height/2

        self.clear()
        self.sprite.draw()
        # self.l.render()
        #self.c.render()
        #self.img_arrow.draw()
        self.figure.draw()

        for drop in self.drops:
            drop.render()
        # self.fps_display.draw()

    # def update(self, dt):
     #   if self.c.y  - self.y_step > 0:
       #     self.c.y -= self.y_step

    # def on_mouse_motion(self, x, y, dx, dy):
        # nothing to do here if not in debug
        # print x, y

    def run(self, callback=lambda s: None):
        self.thread = threading.Thread(target=callback)
        self.thread.setDaemon(True)
        self.thread.start()
        pyglet.app.run()

    def dropTo(self, x, y):
        self.drops.append(
            primitives.Circle(
                self.mapX(x), self.mapY(y), width=self.y_step, color=(
                    0., .9, 0., 1.)))

    def drop(self):
        (x, y) = self.direction
        self.dropTo(self.x + x, self.y + y)
        return (self.x + x, self.y + y)

    def setDirection(self, direction):
        self.direction = direction
        # this is a hack, since we only rotate left atm:
        self.img_arrow.rotation = (self.img_arrow.rotation - 90) % 360
        print self.img_arrow.rotation
        self.figure = self.figures[self.img_arrow.rotation]

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        return self.moveBy(self.direction)

    def moveBy(self, direction):
        (x, y) = direction
        success = True
        if self.y + y >= 0 and self.y + y < self.map.rows:
            self.y += y
        else:
            success = False

        if self.x + x >= 0 and self.x + x < self.map.cols:
            self.x += x
        else:
            success = False

        time.sleep(0.2)
        return success

if __name__ == '__main__':
    TschunkView(TschunkMap1())
    sys.exit(pyglet.app.run())
