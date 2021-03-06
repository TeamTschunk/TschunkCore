import random
from TschunkView import *
from CodeView import *

# Command Values
# 1 ... Left
# 3 ... Straight
# 4 ... Non Operation
# 5 ... Drop
# 6 ... Start
# 7 ... Stop


class game(object):

    def __init__(self):
        self.map = TschunkMap1()
        self.codeView = CodeView()
        self.mapView = TschunkView(self.map)
        self.direction = 0
        self.droppedLetters = []

    def perform_step(self, commands_graph, current_tile, previous_tile):

        self.codeView.updateCode(commands_graph, current_tile)

        command = commands_graph.valueForPosition(current_tile)

        if command == 1:  # rotate left
            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            self.direction = (self.direction + 1) % 4
            self.mapView.setDirection(directions[self.direction])
            #print 'rotated left'
        elif command == 3:  # streight
            if not self.mapView.move() or not self.mapView.move() or not self.mapView.move():
                print 'Game Over'
                return (-1, -1)
            #print 'went straight'
        elif command == 4:
            #print 'did nothing'
            pass
        elif command == 5:
            dropedTo = self.mapView.drop()
            self.droppedLetters.append(dropedTo)
            #print 'dropped'

        if sorted(self.droppedLetters) == sorted(self.map.postBoxes):
            print 'Every Letter delivered'
            return (-1, -1)

        neighbors = commands_graph.neighbors(current_tile)
        if previous_tile in neighbors:
            neighbors.remove(previous_tile)

        preferred = []
        for neighbor in neighbors:
            if commands_graph.valueForPosition(neighbor) != 4:
                preferred.append(neighbor)

        if len(preferred) > 0:
            selected = random.choice(preferred)
            if commands_graph.valueForPosition(selected) != 7:
                return selected

        if len(neighbors) > 0:
            selected = random.choice(neighbors)
            if commands_graph.valueForPosition(selected) != 7:
                return selected

        return (-1, -1)
