from random import shuffle

class EmptyResourcePoolException(Exception):
    pass

class ResourcePool:
    def draw(self, window):
        raise NotImplementedError('Subclass {c} of ResourcePool must implement draw method.'.format(c=self.__class__.__name__))

class CardPool(ResourcePool):
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

class Deck(CardPool):
    DECK_THICKNESS = 5
    def draw(self):
        if not self.cards: return
        
        glPushMatrix()
        
        for card in reversed(self.cards[:Deck.DECK_THICKNESS]):
            card.cardback.draw()
            
            glTranslatef(2, 2, 0)
        
        glPopMatrix()

class Hand(CardPool):
    def draw(self, center_offset=0, degrees_between_cards=8.5):
        if not self.cards: return
        
        glPushMatrix()
        
        if center_offset:
            glTranslatef(0, -center_offset, 0)
        
        glRotatef(degrees_between_cards * ceil(len(self.cards) / 2), 0, 0, 1)
        
        for card in self.cards:
            
            glPushMatrix()        
        
            if center_offset:
                glTranslatef(0, center_offset, 0)
                
            card.draw()
            
            glPopMatrix()
            
            glRotatef(-degrees_between_cards, 0, 0, 1)
            
        
        glPopMatrix()
        