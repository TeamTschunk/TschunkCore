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
        self.commands = self.vision.get_commands_array()
        self.current_tile = self.get_launch_tile()
        self.main_loop()
    
    def main_loop(self):
        while self.current_tile > (-1,-1):
            self.visualizer.visualize_position(self.current_tile)
            self.current_tile = self.game.perform_step(self.commands, self.current_tile)
            sleep(1)
            self.commands = self.generate_commands_graph()
        
    def get_launch_tile(self):
        return (5,5)
    
    def generate_commands_graph(self):
        return self.vision.get_commands_array()
    
    
    