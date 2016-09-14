"""Love Letter Clone

Usage: python -m BGL.samples.LoveLetter.loveletter

"""

from collections import defaultdict
from os.path import dirname, join, realpath

from ...bgl import bgl


def main(**kwargs):
    bg_path = join(dirname(realpath(__file__)), 'resources', 'loveletter.json')
    
    # board = bgl.loader.load_board(bg_path, loader.MonopolyGraphLoader)
    
    bgl.run()
    

if __name__ == '__main__':
    main()