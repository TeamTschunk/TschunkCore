from vision import vision
from visualizer import visualizer
from time import sleep

class tschunk(object):
    def __init__(self, game):
        self.vision = vision()
        self.visualizer = visualizer()
        self.current_tile = (0,0)
        self.game = game

    def run(self):
        commands_array = self.vision.get_commands_array()
        self.command_graph = command_graph(commands_array)
        self.current_tile = self.get_launch_tile()
        self.previous_tile = (-1,-1)
        self.main_loop()

    def main_loop(self):
        while self.current_tile > (-1,-1):
            self.visualizer.visualize_position(self.current_tile)
            prev = self.previous_tile
            self.previous_tile = self.current_tile
            sleep(0.5)
            self.current_tile = self.game.perform_step(self.command_graph, self.current_tile, prev)
            commands_array = self.vision.get_commands_array()
            self.command_graph = command_graph(commands_array)

    def get_launch_tile(self):
        return (0,0)

    def generate_commands_graph(self):
        return self.vision.get_commands_array()

class command_graph(object):

    def __init__(self, command_array):
        self.array = command_array

    def neighbors(self, position):
        x = position[0]
        y = position[1]

        size = len(self.array) -1

        neighbors = []
        if (x > 0 and self.array[x-1][y] > 0):
            neighbors += [(x-1,y)]
        if (x < size and self.array[x+1][y] > 0):
            neighbors += [(x+1,y)]
        if (y > 0 and self.array[x][y-1] > 0):
            neighbors += [(x,y-1)]
        if (y < size and self.array[x][y+1] > 0):
            neighbors += [(x,y+1)]

        return neighbors

    def valueForPosition(self, position):
        return self.array[position[0]][position[1]]


