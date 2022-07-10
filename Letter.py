import pygame
import math

MAX_CONNECT_DIST_MOD = 1.5 #multiplied times font size
MAX_CONNECT_ANGLE = 0.6 * math.pi #out of 1 pi


class Letter:

    def __init__(self, char, x, y, font_size):

        self.radius = font_size

        self.char=char #string
        self.font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self.color=(100, 100, 100)
        self.rect=self.font.render(char, True, self.color).get_rect()
        self.rect.center=(x, y)
        self.connected=False

    def coords(self):
        return self.rect.center
    
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
        return dist < self.radius*MAX_CONNECT_DIST_MOD and abs(theta) < MAX_CONNECT_ANGLE