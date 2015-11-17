
class TschunkMap1():  # (TschunkMap):

    def __init__(self):
        self.img = 'games/postmeister/img/map1.png'
        self.figure = 'todo'

        self.rows = 15
        self.cols = 8

        self.origin_x = 1
        self.origin_y = 14

        self.initial_direction = (0, -1)
        self.postBoxes = [(5, 2), (5, 5), (5, 8), (5, 11)]
