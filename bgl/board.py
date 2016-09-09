class Board:

    def draw(self, window, graph=None):
        if graph is not None:
            self.graph.draw(window)
        
    def __init__(self, graph=None):
        self.graph = graph