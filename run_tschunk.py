from tschunk import tschunk
from games.postmeister import game
import threading
import pyglet

# modulename = "sample"
# game_module = __import__("games." + modulename, fromlist=['blah'])

game = game.game()


t = tschunk.tschunk(game)

thread = threading.Thread(target=t.run)
thread.setDaemon(True)
thread.start()
pyglet.app.run()
