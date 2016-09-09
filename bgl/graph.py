import pyglet

class GraphNode:
    def draw(self, window):
        '''Draw the node.  Assumes node size of 1 and position of (0, 0).'''
        if self.pos is None:
            return
        glLoadIdentity()
        
        x, y = self.pos
        s, sx, sy = window.get_scale()
        
        glTranslatef(x, y, 0)
        glScalef(sx, sy, 1)

        x, y = (0, 0)
        x2, y2 = (1, 1)
        r, g, b = self.rgb
        pyglet.graphics.draw(4, GL_QUADS,
            ('v2f', [x, y, x2, y, x2, y2, x, y2]),
            ('c3B', [r, g, b,
                     r, g, b,
                     r, g, b,
                     r, g, b])
        )
        
        r, g, b = (0, 0, 0)
        pyglet.graphics.draw(4, GL_LINE_LOOP,
            ('v2f', [x, y, x2, y, x2, y2, x, y2]),
            ('c3B', [r, g, b,
                     r, g, b,
                     r, g, b,
                     r, g, b])
        )
    

    def __init__(self, pos=None, gv_label=None, adj=None, tiletype=None, rgb=None):
        if adj is None:
            adj = []
        if rgb is None:
            rgb = (100, 100, 100)

        self.pos = pos
        self.gv_label = gv_label
        self.adj = adj
        self.tiletype = tiletype
        self.rgb = rgb

class Graph:
    def draw(self, window):
        for node in self.nodes:
            glPushMatrix()
            node.draw(window)
            glPopMatrix()

    def __init__(self, nodes):
        self.nodes = nodes