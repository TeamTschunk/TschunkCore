from tschunk import tschunk
from games.sample import game

# modulename = "sample"
# game_module = __import__("games." + modulename, fromlist=['blah'])

game = game.game()

t = tschunk.tschunk(game)
t.run()