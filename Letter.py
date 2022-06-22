import pygame
import math

MAX_CONNECT_DIST_MOD = 1.5 #multiplied times font size
MAX_CONNECT_ANGLE = 0.6 * math.pi #out of 1 pi


class Letter:
    font_size=10

    def __init__(self, char, x, y):
        self.char=char #string
        self.font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self.color=(100, 100, 100)
        self.rect=self.font.render(char, True, self.color).get_rect()
        self.rect.center=(x, y)
        self.connected=False

        #self.text_red = self.font.render(char, True, (255, 0, 0))

        '''self.colors = []
        self.colors.append((255, 0, 0))
        self.colors.append((0, 255, 0))
        self.colors.append((0, 0, 255))
        self.colors.append((127, 127, 0))
        self.colors.append((127, 0, 127))
        self.colors.append((0, 127, 127))

        self.font_variations = []
        for color in self.colors:
            self.font_variations.append(self.font.render(char, True, color))'''

    def coords(self):
        return self.rect.center

    '''def with_color(self, col):
        if col==-1:
            self.color=(100, 100, 100)
        else:
            self.color=colors[col % len(self.colors)]
            #return self.font_variations[color % len(self.colors)]
        return self.font.render(self.char, True, self.color)'''
    
    def generate_font(self):
        if self.connected==True:
            return self.font.render(self.char, True, self.color)
        else:
            return self.font.render(self.char, True, (100, 100, 100))

    def isAdjacentAndLeft(self, letter2):
        (x,y) = self.coords()
        (x2, y2) = letter2.coords()
        dist = math.hypot(x2-x, y2-y)
        theta = math.atan2(y2-y, x2-x)
        return dist < font_size*MAX_CONNECT_DIST_MOD and abs(theta) < MAX_CONNECT_ANGLE

        # isLeft = self.rect.x < letter2.rect.x
        # adjacentHorizontally = abs(self.rect.x-letter2.rect.x)<(font_size*MAX_CONNECT_DIST_MOD)
        # adjacentVertically = abs(self.rect.y-letter2.rect.y)<(font_size*MAX_CONNECT_DIST_MOD)
