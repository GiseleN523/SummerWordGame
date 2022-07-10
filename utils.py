import pygame
from pygame import Rect

# Events
class GameEvent:
    StartGame = pygame.USEREVENT + 1
    GameOver = pygame.USEREVENT + 2
    # Quit just uses the default pygame event


class GameFonts:
    def __init__(self, screen):
        min_screen_distance = min(screen.get_width(), screen.get_height())
        header_font_size = int(min_screen_distance / 10)
        paragraph_font_size = int(min_screen_distance / 20)
        button_font_size = int(min_screen_distance / 15)
        
        debug_font_size = int(min_screen_distance / 30)

        self.header = pygame.font.SysFont('freesanbold.ttf', header_font_size)
        self.paragraph = pygame.font.SysFont('freesanbold.ttf', paragraph_font_size)
        self.button = pygame.font.SysFont('freesanbold.ttf', button_font_size)
        self.debug = pygame.font.SysFont('freesanbold.ttf', debug_font_size)

class CommonGui:
    def __init__(self, screen):
        self.popup=Rect(75, 75, screen.get_width()-150, screen.get_height()-150)

class GameInput:
    def __init__(self, mouse_x, mouse_y, mouse_hold_down, mouse_click_down):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.mouse_hold_down = mouse_hold_down
        self.mouse_click_down = mouse_click_down
