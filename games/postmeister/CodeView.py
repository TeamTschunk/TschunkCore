import sys
import pyglet
from pyglet.gl import *
import primitives
import utils
from map1 import *
import threading

FPS = 60
smoothConfig = utils.getSmoothConfig()

class CodeView(pyglet.window.Window):

    def mapX(self, x):
        return  x * self.width / self.cols

    def mapY(self, y):
        return (self.height - self.op_left.height) - y * self.height / self.rows

    def __init__(self):
        super(
            CodeView,
            self).__init__(
            fullscreen=False,
            caption='Code!',
            config=smoothConfig)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        drop  = pyglet.resource.image('games/postmeister/img/op_drop.png')
        self.op_drop  = pyglet.sprite.Sprite(drop)

        left  = pyglet.resource.image('games/postmeister/img/op_left.png')
        self.op_left  = pyglet.sprite.Sprite(left)

        nop  = pyglet.resource.image('games/postmeister/img/op_nop.png')
        self.op_nop  = pyglet.sprite.Sprite(nop)

        straight  = pyglet.resource.image('games/postmeister/img/op_straight.png')
        self.op_straight  = pyglet.sprite.Sprite(straight)

        self.initialized = False

        # Setup debug framerate display:
        self.fps_display = pyglet.clock.ClockDisplay()

        # Schedule the update of this window, so it will advance in time at the
        # defined framerate.  If we don't, the window will only update on events
        # like mouse motion.

        #pyglet.clock.schedule_interval(self.update, 1.0)

        self.width = 1000
        self.height = 600
        self.rows = 4
        self.cols = 4
        self.set_size(self.width, self.height)
        self.set_location(20, 20)

    def on_draw(self):
        if not self.initialized:
            return

        self.op_left.scale = (self.width/self.cols)/500.
        self.op_nop.scale = (self.width/self.cols)/500.
        self.op_drop.scale = (self.width/self.cols)/500.
        self.op_straight.scale = (self.width/self.cols)/500.
        self.height = int(self.width * (600./1000.))

        for x in range(0, self.cols):
            for y in range(0, self.rows):

                command = self.array[x][y]
                print x, ',', y, ' is ', command

                if command == 1:  # rotate left
                    self.op_left.x = self.mapX(x)
                    self.op_left.y = self.mapY(y)
                    self.op_left.draw()
                elif command == 3:  # straight
                    self.op_straight.x = self.mapX(x)
                    self.op_straight.y = self.mapY(y)
                    self.op_straight.draw()
                elif command == 4: # nop
                    self.op_nop.x = self.mapX(x)
                    self.op_nop.y = self.mapY(y)
                    self.op_nop.draw()
                elif command == 5: # dropping
                    self.op_drop.x = self.mapX(x)
                    self.op_drop.y = self.mapY(y)
                    self.op_drop.draw()

        (x, y) = self.current
        tile_height = self.op_left.height
        tile_width = self.op_left.width

        rect = primitives.Polygon([(self.mapX(x), self.mapY(y)),
                                        (self.mapX(x), self.mapY(y) + tile_height),
                                        (self.mapX(x) + tile_width, self.mapY(y) + tile_height),
                                        (self.mapX(x) + tile_width, self.mapY(y))
                                         ],color=(.3, 0.2, 0.5, .7))
        rect.render()

        #self.op_left.x = self.mapX(0)
        #self.op_left.y = self.mapY(0)
        #self.op_left.draw()


    def updateCode(self, commands_graph, current_tile):
        self.rows = len(commands_graph.array)
        self.cols = len(commands_graph.array[0])

        self.array = commands_graph.array
        self.current = current_tile

        self.initialized= True

