import random
import os

class game(object):

    def __init__(self):
        pass

    def perform_step(self, commands_graph, current_tile, previous_tile):
        neighbors = commands_graph.neighbors(current_tile)
        if previous_tile in neighbors:
            neighbors.remove(previous_tile)
            
        value = commands_graph.valueForPosition(current_tile)
        self.beep(value)

        if len(neighbors) > 0:
            selected = random.choice(neighbors)
            if commands_graph.valueForPosition(selected) != 7:
                return selected

        return previous_tile
    
    def beep(self, value):
        
        notes = [262, 294, 330, 349, 392, 440, 494]
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.5, notes[value]))