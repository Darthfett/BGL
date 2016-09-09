events = {}

class Event:
    def fire(self, gamestate):
        print('{name} event fired -->'.format(name=self.name))
        for rule in self.rules:
            rule.on_event(self, gamestate)
        print('<-- {name} event resolved'.format(name=self.name))
    
    def subscribe(self, rule):
        self.rules.append(rule)
    
    def __init__(self, name, rules=None):
        if rules is None:
            rules = []
            
        self.name = name
        self.rules = rules
        
        events[name] = self

Event('StartGame')