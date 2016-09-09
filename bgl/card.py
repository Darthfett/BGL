
class BaseCard: pass

class Card:
    def __init__(self, base_card, reqs, effects):
        self.base_card = base_card
        self.reqs = reqs
        self.effects = effects