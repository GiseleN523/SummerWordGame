import pygame
from pygame.locals import *

import random
import math
import time
import enum

import WordGenerator
import Letter
import Gameplay

import start_screen
import end_screen

"""
TO DO
-when to add words to list? each time one is formed or when timer runs out (current method)
-should letters also need to be above letters they come before, the way they need to be to their left?
-more languages
-special abilities when you form certain words (palindromes, >5 letters, etc): choose any letter, slow down time, hint, etc

(it's better now that we're not starting out with words, but it can still get pretty bad even if you have like 4-5 really short words)
What is causing it to be so slow?
-two recursive methods (calculate_all_adjacent_strings() and get_best_combo)?
-determining color for each letter?
"""

class Scene(enum.Enum):
    StartScreen = 1
    Playing = 2
    EndScreen = 3


class Fonts:
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


def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Our Game")
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((640, 360)) #test resolution
    clock = pygame.time.Clock()

    scr_width = screen.get_width()
    scr_height = screen.get_height()
    print("Screen dimensions ", scr_width, "x", scr_height)
    
    # === TUNABLE SETTINGS ===
    Letter.font_size=int(min(scr_width, scr_height) / 10)

    game_scene = "start_screen"
    fonts = Fonts(screen)
    common_gui = CommonGui(screen)


    # print("Font size: ", font_size)
    font_spacing = int(0.5 * Letter.font_size)  #TODO: make this use internal font spacing
    
    #words_raw = generator.get_random_word_list(2)
    
    
    #available_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (127, 127, 0), (127, 0, 127), (0, 127, 127)]

    running = True

    mouse_hold_down = False
    

    gameplay = Gameplay.Gameplay()


    while running:
        # === INPUT ===
        mousex, mousey = pygame.mouse.get_pos()
        mouse_click_down = False
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_down = True
                mouse_hold_down = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_hold_down = False

        game_input = GameInput(mousex, mousey, mouse_hold_down, mouse_click_down)
        

        # === GAME LOGIC and RENDER ===
        # clear display
        screen.fill((255, 255, 255))
        
        if game_scene == "start_screen":
            next_scene = start_screen.start_screen(screen, game_input, fonts, common_gui)

            if next_scene:
                game_scene = "playing"                
                gameplay.on_game_start(screen)
        
        elif game_scene == "playing":
            next_scene = gameplay.playing(screen, game_input, fonts, common_gui)

            if next_scene:
                game_scene = "end_screen"
                
        elif game_scene == "end_screen":

            (next_scene, next_scene_name) = end_screen.end_screen(screen, game_input, fonts, common_gui)

            if next_scene:
                if next_scene_name == "playing":
                    game_scene = next_scene_name
                    gameplay.on_game_start(screen)
                elif next_scene_name == "quit":
                    running = False
        
        
        pygame.display.flip()

        # limit frames per second
        clock.tick(60)


        
if __name__=="__main__":
    main()