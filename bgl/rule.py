events = {}
conditions = {}
actions = {}
rules = {}

class Rule:
    
    def get_actions(event):
        try:
            return self.actions.get(event)
        except AttributeError:
            return self.actions
    
    def evaluate_conditions(self, event):
        if self.conditions is None:
            return True
        if all(condition(event, gamestate) for condition in self.conditions):
            return True
        return False

    def on_event(self, event, gamestate):
        print('{name} rule activated'.format(name=self.name))
        if event in self.events:
            if self.evaluate_conditions(event, gamestate):
                actions = self.get_actions(event)
                for action in actions:
                    action(gamestate)
        return None

    def __init__(self, name, events=None, conditions=None, actions=None):
        self.name = name
        self.events = events
        self.conditions = conditions
        self.actions = actions
        
        for ev in events:
            ev.subscribe(self)
        
        rules[name] = self

# EVENTS

class Event:
    def __call__(self, gamestate):
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

# CONDITIONS

class Condition:
    def __init__(self, name):
        self.name = name
        conditions[name] = self

class BoolCondition(Condition):
    def __init__(self, name, value=False):
        super().__init__(name)
        self.value = value

# ACTIONS

def choose_node(player, nodes):
    print('{pname}, choose a node:'.format(pname=player.name))
    
    choices = [node.name for node in nodes]
    print('\n\t'.join(choices))
    choice = input(': ')
    while choice not in choices:
        print('Invalid choice.')
        print('{pname}, choose a node:'.format(pname=player.name))
        print('\n\t'.join(choices))
        choice = input(': ')
    return nodes[choices.index(choice)]

def move_pawn(pawn, distance=1):
    adj = pawn.node.adj
    nadj = pawn.node.nadj

    while distance > 0:
        if len(adj) == 0:
            return
        elif len(adj) == 1:
            pawn.node = adj[0]
        elif len(adj) > 1:
            pawn.node = choose_node(pawn.owner, adj)
        distance += 1
    while distance < 0:
        if len(nadj) == 0:
            return
        elif len(nadj) == 1:
            pawn.node = nadj[0]
        elif len(nadj) > 1:
            pawn.node = choose_node(pawn.owner, nadj)
        distance -= 1

class ActionLoader:
    def __init__(self, act_def):
        self.action_definition = act_def

class MovePlayerPawn(ActionLoader):
    def __call__(self, gamestate):
        if self.space is not None:
            pawn = gamestate.current_player.pawn
            pawn.node = gamestate.graph[self.space]
        if self.distance is not None:
            pawn = gamestate.current_player.pawn
            move_pawn(pawn, self.distance)
            
    def __init__(self, act_def):
        super().__init__(act_def)
        if 'space' in act_def:
            self.space = act_def['space']
        else:
            self.space = None
        if 'distance' in act_def:
            self.distance = act_def['distance']

actions['move_player_pawn'] = MovePlayerPawn