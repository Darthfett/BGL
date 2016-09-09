
from pyglet.gl import *

from ...bgl import bgl
import math

class MonopolyNode(bgl.graph.GraphNode):
    def draw_title(self, window):
        if self._name_label is None:
            s, sx, sy = window.get_scale()
            self._name_label = pyglet.text.Label(self.name,
                font_name='Times New Roman',
                font_size=9,
                x=2, y=sy,
                width=sx, height=sy,
                multiline=True,
                anchor_x='left', anchor_y='top'
            )
        
        self._name_label.draw()
        
    def draw_cost(self, window):
        pass
    
    def draw_label(self, window):
        if self.gv_label is not None:
            if self._label is None:
                s, sx, sy = window.get_scale()
                self._label = pyglet.text.Label(self.gv_label,
                    font_name='Times New Roman',
                    font_size=9,
                    x=sx/2, y=0,
                    width=sx, height=sy,
                    anchor_x='center', anchor_y='center'
                )
                
            self._label.draw()
        
    def draw(self, window):
        glLoadIdentity()
        
        x, y = self.pos
        s, sx, sy = window.get_scale()
        
        if (y == 0) or ((x + y) in (0, 10, 20)):
            # If at one of the four corners, or on the bottom row, don't rotate
            glTranslatef(x * sx, y * sy, 0)
        elif y == 10:
            glTranslatef((x + 1) * sx, (y + 1) * sy, 0)
            glRotatef(180, 0, 0, 1)
        elif x == 0:
            glTranslatef(x * sx, (y + 1) * sy, 0)
            glRotatef(270, 0, 0, 1)
        elif x == 10:
            glTranslatef((x + 1) * sx, y * sy, 0)
            glRotatef(90, 0, 0, 1)
        
        x1, y1 = (0, 0)
        x2, y2 = (sx, sy)
        
        r, g, b = (100, 100, 100)
        pyglet.graphics.draw(4, GL_QUADS,
            ('v2f', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c3B', [r, g, b,
                     r, g, b,
                     r, g, b,
                     r, g, b])
        )
        
        r, g, b = (0, 0, 0)
        pyglet.graphics.draw(4, GL_LINE_LOOP,
            ('v2f', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c3B', [r, g, b,
                     r, g, b,
                     r, g, b,
                     r, g, b])
        )
        
        self.draw_title(window)
        self.draw_cost(window)
            
        
    def __init__(self, *args, name, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._name_label = None
        self._label = None

class PropertyNode(MonopolyNode):
    def draw_title(self, window):
        x, y = self.pos
        s, sx, sy = window.get_scale()
        
        name_label = pyglet.text.Label(self.name,
            font_name='Times New Roman',
            font_size=9,
            x=2, y=(0.8 * sy),
            width=sx, height=sy,
            multiline=True,
            anchor_x='left', anchor_y='top'
        )
        name_label.draw()

    def draw_cost(self, window):
        x, y = self.pos
        s, sx, sy = window.get_scale()

        cost_label = pyglet.text.Label(self.cost,
            font_name='Times New Roman',
            font_size=12,
            x=((0.5) * sx), y=0,
            anchor_x='center', anchor_y='bottom'
        )
        cost_label.draw()

    def draw(self, window):
        glPushMatrix()
        super().draw(window)
        
        s, sx, sy = window.get_scale()
        x1, y1 = (1, (0.85*sy))
        x2, y2 = (sx-1, sy-1)
        
        r, g, b = self.rgb    
        pyglet.graphics.draw(4, GL_QUADS,
            ('v2f', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c3B', [r, g, b,
                     r, g, b,
                     r, g, b,
                     r, g, b])
        )
        glPopMatrix()
        
    def __init__(self, *args, cost, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = cost

class PurpleNode(PropertyNode):
    def __init__(self, *args, rgb=(100, 0, 100), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class LightBlueNode(PropertyNode):
    def __init__(self, *args, rgb=(100, 160, 255), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class PinkNode(PropertyNode):
    def __init__(self, *args, rgb=(255, 100, 150), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class OrangeNode(PropertyNode):
    def __init__(self, *args, rgb=(255, 100, 50), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class RedNode(PropertyNode):
    def __init__(self, *args, rgb=(255, 0, 0), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class YellowNode(PropertyNode):
    def __init__(self, *args, rgb=(200, 200, 0), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class GreenNode(PropertyNode):
    def __init__(self, *args, rgb=(0, 150, 0), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class DarkBlueNode(PropertyNode):
    def __init__(self, *args, rgb=(20, 20, 150), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class RailRoadNode(PropertyNode):
    def __init__(self, *args, rgb=(60, 60, 60), **kwargs):
        super().__init__(*args, rgb=rgb, **kwargs)

class GoNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommunityChestNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class IncomeTaxNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ChanceNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InJailNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class JustVisitingNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FreeParkingNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ElectricCompanyNode(PropertyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class WaterWorksNode(PropertyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GoToJailNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LuxuryTaxNode(MonopolyNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
tiletype_map = {
    'Purple':    PurpleNode, 
    'LightBlue': LightBlueNode,
    'Pink':      PinkNode,
    'Orange':    OrangeNode,
    'Red':       RedNode,
    'Yellow':    YellowNode,
    'Green':     GreenNode,
    'DarkBlue':  DarkBlueNode,
    'RailRoad':  RailRoadNode,
    
    'Go':              GoNode,
    'CommunityChest':  CommunityChestNode,
    'IncomeTax':       IncomeTaxNode,
    'Chance':          ChanceNode,
    'InJail':          InJailNode,
    'JustVisiting':    JustVisitingNode,
    'FreeParking':     FreeParkingNode,
    'ElectricCompany': ElectricCompanyNode,
    'WaterWorks':      WaterWorksNode,
    'GoToJail':        GoToJailNode,
    'LuxuryTax':       LuxuryTaxNode,
}