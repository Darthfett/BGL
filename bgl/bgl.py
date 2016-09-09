"""Board Game Library

Usage: bgl.py [-h --version] [--board=FILE [--rules=FILE]] [--debug]

Options:
  -h --help     Show this message.
  --version     Show version number.
  --board=FILE  Specify the board map to play on.
  --rules=FILE  Specify rules
  --debug       Operate in debug mode.

"""

import re
import sys

from docopt import docopt
import pyglet
from pyglet.gl import *

from . import board
from . import card
from . import event
from . import graph
from . import loader
from . import resource
from . import rule
from . import tiletypes

import random

__all__ = ['board', 'card', 'event', 'graph', 'loader', 'resource', 'rule', 'tiletypes']

class BGLWindow(pyglet.window.Window):
    def get_scale(self):
        s = min([self.width * 0.8, self.height])
        drawable_nodes = [node for node in self.board.graph.nodes if node.pos is not None]
        sx = s / (max(node.pos[0] for node in drawable_nodes) - min(node.pos[0] for node in drawable_nodes) + 1)
        sy = s / (max(node.pos[1] for node in drawable_nodes) - min(node.pos[1] for node in drawable_nodes) + 1)
        return s, sx, sy

    def on_draw(self):
        glLoadIdentity()
        
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        
        glPushMatrix()
        self.board.draw(self)
        glPopMatrix()
        
        self.fps_display.draw()
    
    def update(self, dt):
        pass
    
    def run(self):
        rule.events['StartGame'](self)
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()
    
        
    def __init__(self, *args, board, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.fps_display = pyglet.clock.ClockDisplay()


def get_usage():
    global usage
    try:
        usage
    except NameError:
        pattern = re.compile('^([^\n]*usage:[^\n]*\n?(?:[ \t].*?(?:\n|$))*)',
                             re.IGNORECASE | re.MULTILINE)
        usage = pattern.findall(__doc__)[0].strip()
    return usage

def run(board):
    window = BGLWindow(1200, 900, board=board)
    window.run()


def main(**kwargs):
    if kwargs['--debug']:
        print('Debugging...')
    
    if kwargs['--board'] is None:
        print(get_usage())
        sys.exit(-1)
        
    bg_path = kwargs['--board']
    
    board = loader.load_board(bg_path)
    
    run(board)


if __name__ == '__main__':
    args = docopt(__doc__, version='Board Game Library v0.0.1')
    
    main(**args)