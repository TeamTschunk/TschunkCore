import random

class game(object):
    
    def __init__(self):
        pass
    
    def perform_step(self, commands_graph, current_tile, previous_tile):
        neighbors = commands_graph.neighbors(current_tile)
        if previous_tile in neighbors:
            neighbors.remove(previous_tile)
        
        if len(neighbors) > 0 :
            r_neighbor = random.choice(neighbors)
            if commands_graph.valueForPosition(r_neighbor) != 5:
                return r_neighbor
        return (-1,-1)