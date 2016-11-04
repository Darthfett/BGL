

class StandardCard:
    Font_Size = 18
    Font_Size_Pic = 30
    Card_Width = 125
    Card_Height = 175

    w = Card_Width / 6
    h = Card_Height / 6

    rank_to_layout = {
        'A': [(w*3, h*3)],
        '2': [(w*3, h*5),
              (w*3, h*1)],
        '3': [(w*3, h*5),
              (w*3, h*3),
              (w*3, h*1)],
        '4': [(w*2, h*5), (w*4, h*5),
              (w*2, h*1), (w*4, h*1)],
        '5': [(w*2, h*5), (w*4, h*5),
                    (w*3, h*3),
              (w*2, h*1), (w*4, h*1)],
        '6': [(w*2, h*5), (w*4, h*5),
              (w*2, h*3), (w*4, h*3),
              (w*2, h*1), (w*4, h*1)],
        '7': [(w*2, h*5), (w*4, h*5),
                    (w*3, h*4),
              (w*2, h*3), (w*4, h*3),
              (w*2, h*1), (w*4, h*1)],
        '8': [(w*2, h*5), (w*4, h*5),
                    (w*3, h*4),
              (w*2, h*3), (w*4, h*3),
                    (w*3, h*2),
              (w*2, h*1), (w*4, h*1)],
        '9': [(w*2, h*5), (w*4, h*5),
              (w*2, h*4), (w*4, h*4),
                    (w*3, h*3),
              (w*2, h*2), (w*4, h*2),
              (w*2, h*1), (w*4, h*1)],
        '10': [(w*2, h*5), (w*4, h*5),
                    (w*3, h*4.25),
              (w*2, h*3.5), (w*4, h*3.5),
              (w*2, h*2.5), (w*4, h*2.5),
                    (w*3, h*1.75),
              (w*2, h*1), (w*4, h*1)],
        'J': [],
        'Q': [],
        'K': [],
    }
    Ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    Suits = ['♦','♣','♥','♠']
    Suit_Colors = [(255, 0, 0, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255)]

    del w
    del h

    def draw(self, front=True):
        if not front:
            self.cardback.draw()
            return
        
        glColor3f(1,1,1)
        x, dx = 0, StandardCard.Card_Width
        y, dy = 0, StandardCard.Card_Height
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x+dx, y, x+dx, y+dy, x, y+dy]))
        
        glColor3f(0,0,0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x+dx, y)
        glVertex2f(x+dx, y+dy)
        glVertex2f(x, y+dy)
        glEnd()
            
            
        glPushMatrix()
        
        color = StandardCard.Suit_Colors[StandardCard.Suits.index(self.suit)]
            
        topleft_lbl = pyglet.text.Label(self.rank + '\n' + self.suit,
            font_name='Times New Roman',
            font_size=StandardCard.Font_Size,
            x=2, y=StandardCard.Card_Height,
            multiline=True, width=StandardCard.Font_Size,
            color=color,
            anchor_x='left', anchor_y='top'
        )
        topleft_lbl.draw()
        
        for x, y in StandardCard.rank_to_layout[self.rank]:
            lbl = pyglet.text.Label(self.suit,
                    font_name='Times New Roman',
                    font_size=StandardCard.Font_Size_Pic,
                    x=x, y=y,
                    color=color,
                    anchor_x='center', anchor_y='center'
            )
            lbl.draw()
            
        
        glRotatef(180, 0, 0, 1)
        
        bottomright_lbl = pyglet.text.Label(self.rank + '\n' + self.suit,
            font_name='Times New Roman',
            font_size=StandardCard.Font_Size,
            x=-StandardCard.Card_Width+2, y=0,
            multiline=True, width=StandardCard.Font_Size,
            color=color,
            anchor_x='left', anchor_y='top'
        )
        
        bottomright_lbl.draw()
        glPopMatrix()

    def __init__(self, rank, suit, cardback):
        self.rank = rank
        self.suit = suit
        self.cardback = cardback