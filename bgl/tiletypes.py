tiletypes = {}

class Tiletype:
    def __init__(self, name):
        self.name = name
        
        tiletypes[name] = self