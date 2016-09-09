"""Monopoly Clone

Usage: python -m BGL.samples.Monopoly.monopoly [-h --version --debug]

Options:
  -h --help     Show this message.
  --version     Show version number.
  --debug       Operate in debug mode.

"""

from collections import defaultdict
from os.path import dirname, join, realpath

#import docopt

from ...bgl import bgl
from ...bgl.bgl import loader
from . import loader


def main(**kwargs):
    bg_path = join(dirname(realpath(__file__)), 'resources', 'monopoly.json')
    
    board = bgl.loader.load_board(bg_path, loader.MonopolyGraphLoader)
    
    bgl.run(board)
    

if __name__ == '__main__':
    #args = docopt.docopt(__doc__, version='Monopoly v0.0.1')
    
    #main(**args)
    main()