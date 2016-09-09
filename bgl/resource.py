from random import shuffle

class EmptyResourcePoolException(Exception):
    pass

class ResourcePool:
    def draw(self, window):
        raise NotImplementedError('Subclass {c} of ResourcePool must implement draw method.'.format(c=self.__class__.__name__))

class Deck(ResourcePool):
    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        raise EmptyResourcePoolException()
    
    def shuffle(self):
        shuffle(self.cards)
        
    def __init__(self, cards=None):
        super().__init__()
        
        if cards is None:
            cards = []
        
        self.cards = cards