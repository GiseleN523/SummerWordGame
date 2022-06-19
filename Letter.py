import pygame

class Letter:
    font_size=10

    def __init__(self, char, x, y):
        self.char=char #string
        self.font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self.color=(100, 100, 100)
        self.text_default = self.font.render(char, True, self.color)
        self.rect=self.text_default.get_rect()
        self.rect.center=(x, y)

        #self.text_red = self.font.render(char, True, (255, 0, 0))

        self.colors = []
        self.colors.append((255, 0, 0))
        self.colors.append((0, 255, 0))
        self.colors.append((0, 0, 255))
        self.colors.append((127, 127, 0))
        self.colors.append((127, 0, 127))
        self.colors.append((0, 127, 127))

        self.font_variations = []
        for color in self.colors:
            self.font_variations.append(self.font.render(char, True, color))

        self.word_id = 0
        
        self.color=(100, 100, 100)

    def coords(self):
        return self.rect.center

    def with_color(self, col):
        if col==-1:
            self.color=(100, 100, 100)
        else:
            self.color=colors[col % len(self.colors)]
            #return self.font_variations[color % len(self.colors)]
        return self.font.render(self.char, True, self.color)
    
    def generate_font(self):
        return self.font.render(self.char, True, self.color)

    def isAdjacentTo(self, letter2):
        if abs(self.rect.x-letter2.rect.x)<(font_size*1) and abs(self.rect.y-letter2.rect.y)<(font_size*1):
            return True
        else:
            return False
