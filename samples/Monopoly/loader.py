
from pyglet.gl import *
import pydotplus as pydot

from ...bgl.bgl import loader
from ...bgl.bgl import graph

from . import nodes

class MonopolyGraph(graph.Graph):
    def draw(self, window):
        for node in self.nodes:
            node.draw(window)
        
        # Draw the game title in the board center
        glLoadIdentity()
        
        s, sx, sy = window.get_scale()
                
        glTranslatef(s/2, s/2, 0)
        glRotatef(45, 0, 0, 1)
        
        
        self.title_label.draw()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_label = pyglet.text.Label("Monopoly",
            font_name='Bauhaus 93',
            font_size=60,
            color=(0, 0, 0, 127),
            x=0, y=0,
            anchor_x='center', anchor_y='center'
        )


class MonopolyGraphLoader(loader.GraphLoader):
    
    def _get_node_map(self, pydot_graph):
        node_map = {}
        for pydot_node in pydot_graph.get_nodes():
            
            pos, gv_label, tiletype = self._get_pydot_node_values(pydot_node)
            
            if gv_label is None:
                node_map[pydot_node.get_name()] = graph.GraphNode(pos=pos, gv_label=gv_label, tiletype=tiletype)
                continue
            elif r'\n' in gv_label:
                name, cost = gv_label.split(r'\n')
                if not cost.startswith('$'):
                    gv_label = cost
                    cost = None
            else:
                name = gv_label
                cost = None
                gv_label = None

            if cost is None:
                graph_node = nodes.tiletype_map[tiletype.name](name=name, pos=pos, gv_label=gv_label, tiletype=tiletype)
            else:
                graph_node = nodes.tiletype_map[tiletype.name](name=name, cost=cost, pos=pos, gv_label=gv_label, tiletype=tiletype)
            
            node_map[pydot_node.get_name()] = graph_node
            
        return node_map
        
    def load(self, dot_data):
        pydot_graph = pydot.graph_from_dot_data(dot_data)
        
        node_map = self._get_node_map(pydot_graph)
        
        self._fix_edges(pydot_graph, node_map)
        
        graph = MonopolyGraph(node_map.values())
        
        return graph
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    