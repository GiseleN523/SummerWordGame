import pygame

class Letter:
    font_size=10
    
    def __init__(self, char, x, y):
        self.char=char #string
        font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self.text=font.render(char, True, (100, 100, 100))
        self.text_hover = font.render(char, True, (25, 25, 25))
        self.rect=self.text.get_rect()
        self.rect.center=(x, y)
        
    def isAdjacentTo(self, letter2):
        if abs(self.rect.x-letter2.rect.x)<(font_size*1) and abs(self.rect.y-letter2.rect.y)<(font_size*1):
            return True
        else:
            return False
