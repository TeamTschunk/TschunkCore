import random
from TschunkView import *

# Command Values
# 1 ... Left
# 3 ... Straight
# 4 ... Non Operation
# 5 ... Drop
# 6 ... Start

class game(object):

    def __init__(self):
        self.mapView = TschunkView(TschunkMap1())
        self.direction = 0

    def perform_step(self, commands_graph, current_tile, previous_tile):
        neighbors = commands_graph.neighbors(current_tile)
        if previous_tile in neighbors:
            neighbors.remove(previous_tile)

        command = commands_graph.valueForPosition(current_tile)

        print command

        if command == 1: # rotate left
            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            self.direction = (self.direction + 1) % 4
            self.mapView.setDirection(directions[self.direction])
            print 'rotated left'
        elif command == 3: # streight
            self.mapView.move()
            self.mapView.move()
            self.mapView.move()
            print 'went straight'
        elif command == 4:
            print 'did nothing'
        elif command == 5:
            self.mapView.drop()
            print 'dropped'

        if len(neighbors) > 0 :
            r_neighbor = random.choice(neighbors)
            if commands_graph.valueForPosition(r_neighbor) != 7:
                return r_neighbor
        return (-1,-1)


