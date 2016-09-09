import pydotplus as pydot

import collections
import json
from os.path import dirname, join, realpath

from .board import Board
from .graph import Graph, GraphNode
from . import rule
from . import tiletypes
from .tiletypes import Tiletype

class TiletypeLoader:
    def load(self, pydot_tiletype_name):
        if pydot_tiletype_name not in tiletypes.tiletypes:
            tiletype = tiletypes.Tiletype(pydot_tiletype_name)
        else:
            tiletype = tiletypes.tiletypes[pydot_tiletype_name]
        return tiletype
        

class CharacterLoader: pass

class RuleLoader:
    def load_condition(self, cond_def):
        if cond_def['type'] in rule.conditions:
            condition_type = rule.conditions[cond_def.type]
            return condition_type(cond_def)
    
    def load_action(self, act_def):
        if act_def['type'] in rule.actions:
            action_type = rule.actions[act_def['type']]
            return action_type(act_def)
    
    def load(self, rules_dict):
        rules = []
        for name, rule_def in rules_dict.items():
            if 'events' in rule_def:
                ev_list = rule_def['events']
                events = []
                for ev in ev_list:
                    if ev in rule.events:
                        event = rule.events[ev]
                    else:
                        event = rule.Event(name=ev)
                    events.append(event)
            else:
                events = []
            
            if 'conditions' in rule_def:
                cond_list = rule_def['conditions']
                conditions = [self.load_condition(c) for c in cond_list]
            else:
                conditions = None
            
            if 'actions' in rule_def:
                act_list = rule_def['actions']
                actions = [self.load_action(a) for a in act_list]
            else:
                actions = None
            
            r = rule.Rule(name, events, conditions, actions)
            rules.append(r)
        return rules
            

class ImageTileDefinition:
    def tiletype_for_color(self, color):
        return self.definition[color]

    def __init__(self, color_to_tiletype_map):
        self.definition = color_to_tiletype_map
        
def get_pydot_node_pos(pydot_node):
    strpos = pydot_node.get_pos()
    if strpos is None:
        return None

    pos = strpos[1:-1].strip()
    x, y = pos.split(',')
    x = int(x.strip())
    y = int(y.strip())
    return (x, y)
    
def get_pydot_node_label(pydot_node):
    text = pydot_node.get_label()
    if text is None:
        return None
    return text.strip('"').strip("'")

def get_pydot_node_tiletype(pydot_node):
    comment = pydot_node.get_comment()
    if comment is None:
        return None
    properties = comment[1:-1].split(';')
    tiletype_loader = TiletypeLoader()
    for property in properties:
        l, r = property.split('=')
        if l.lower() == 'tiletype':
            return tiletype_loader.load(r)

class GraphLoader:
    def _fix_edges(self, pydot_graph, node_map):
        for pydot_edge in pydot_graph.get_edges():
            graph_node_l = node_map[pydot_edge.get_source()]
            graph_node_r = node_map[pydot_edge.get_destination()]
            
            graph_node_l.adj.append(graph_node_r)
    
    def _get_pydot_node_values(self, pydot_node):
        pos = get_pydot_node_pos(pydot_node)
        gv_label = get_pydot_node_label(pydot_node)
        tiletype = get_pydot_node_tiletype(pydot_node)
        
        return pos, gv_label, tiletype
    
    def _get_node_map(self, pydot_graph):
        node_map = {}
        for pydot_node in pydot_graph.get_nodes():
            
            pos, gv_label, tiletype = self._get_pydot_node_values(pydot_node)
            graph_node = GraphNode(pos=pos, gv_label=gv_label, tiletype=tiletype)
            
            node_map[pydot_node.get_name()] = graph_node
            
        return node_map
        
    def load(self, dot_data):
        pydot_graph = pydot.graph_from_dot_data(dot_data)
        
        node_map = self._get_node_map(pydot_graph)
        
        self._fix_edges(pydot_graph, node_map)
        
        graph = Graph(node_map.values())
        
        return graph
        
        
class BoardLoader:
    def _get_def(self, bg_file):
        with open(bg_file, 'r') as f:
            bg_def = json.load(f)
        
        return bg_def
        
    def _get_dot_data(self, bg_file, bg_def):
        
        # Load board
        dot_fname = join(dirname(realpath(bg_file)), bg_def['board'])
        
        with open(dot_fname, 'r') as f:
            dot_data = f.read()
        
        return dot_data
        
    def load(self, bg_file):
        bg_def = self._get_def(bg_file)
        dot_data = self._get_dot_data(bg_file, bg_def)
        
        graph_loader = self.graph_loader()
        graph = graph_loader.load(dot_data)
        
        board = Board(graph)
        
        # Load rules
        rule_loader = self.rule_loader()
        rules = bg_def['rules']
        if isinstance(rules, collections.Mapping):
            rules_dict = rules
        else:
            assert type(rules) is str
            rules_path = join(dirname(bg_file), rules)
            with open(rules_path, 'r') as f:
                rules_dict = json.load(f)
        
        rules = rule_loader.load(rules_dict)
        
        return board
    
    def __init__(self, graph_loader=None, rule_loader=None):
        if graph_loader is None:
            graph_loader = GraphLoader
        if rule_loader is None:
            rule_loader = RuleLoader
        self.graph_loader = graph_loader
        self.rule_loader = rule_loader

def load_board(board_file, graph_loader=None, rule_loader=None):
    brd_ldr = BoardLoader(graph_loader, rule_loader)
    return brd_ldr.load(board_file)