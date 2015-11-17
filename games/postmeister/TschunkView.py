import sys
import pyglet
from pyglet.gl import *
import primitives
import utils
from map1 import *
import threading

FPS = 60
smoothConfig = utils.getSmoothConfig()

class TschunkView(pyglet.window.Window):

    def mapX(self, x):
        return self.cord_origin_x + x * self.x_step

    def mapY(self, y):
        return self.cord_origin_y + y * self.y_step

    def __init__(self, mymap):
        super(TschunkView, self).__init__(fullscreen=False, caption='Tschunk!', config=smoothConfig)

        self.map = mymap

        self.image = pyglet.resource.image(mymap.img)
        self.sprite = pyglet.sprite.Sprite(self.image)

        self.y_step = self.image.height / mymap.rows + 1
        self.x_step = self.image.width / mymap.cols + 1
        self.cord_origin_x = self.x_step/2
        self.cord_origin_y = self.y_step/2

        self.x = mymap.origin_x
        self.y = mymap.origin_y
        start_x = self.mapX(self.x)
        start_y = self.mapY(self.y)

        self.direction = mymap.initial_direction

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #self.l = primitives.Line((0,0),(100,100),stroke=10,color=(1,0,0,1))
        self.c = primitives.Circle(start_x, start_y,width=self.y_step,color=(1.,0.,0.,1.))
        self.drops = []

        # Setup debug framerate display:
        self.fps_display = pyglet.clock.ClockDisplay()

        # Schedule the update of this window, so it will advance in time at the
        # defined framerate.  If we don't, the window will only update on events
        # like mouse motion.

        #pyglet.clock.schedule_interval(self.update, 1.0)

        self.set_size(self.image.width, self.image.height)

    def on_draw(self):
        self.c.x = self.mapX(self.x)
        self.c.y = self.mapY(self.y)

        self.clear()
        self.sprite.draw()
        #self.l.render()
        self.c.render()
        for drop in self.drops:
            drop.render()
        #self.fps_display.draw()

    #def update(self, dt):
     #   if self.c.y  - self.y_step > 0:
       #     self.c.y -= self.y_step

    #def on_mouse_motion(self, x, y, dx, dy):
        # nothing to do here if not in debug
        #print x, y

    def run(self, callback=lambda s:None):
        self.thread = threading.Thread(target=callback)
        self.thread.setDaemon(True)
        self.thread.start()
        pyglet.app.run()

    def dropTo(self, x, y):
        self.drops.append(primitives.Circle(self.mapX(x), self.mapY(y),width=self.y_step,color=(0.,.9,0.,1.)))

    def drop(self):
        (x, y) = self.direction
        self.dropTo(self.x + x, self.y + y)

    def setDirection(self, direction):
        self.direction = direction

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.moveBy(self.direction)

    def moveBy(self, direction):
        (x, y) = direction
        success = False
        if self.y + y > 0 and self.y  + y < self.map.rows:
            self.y += y
            success = True

        if self.x + x > 0 and self.x + x < self.map.cols:
            self.x += x
            success = True

        return success

if __name__ == '__main__':
    TschunkView(TschunkMap1())
    sys.exit(pyglet.app.run())


