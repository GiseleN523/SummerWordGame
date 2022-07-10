import pygame
from pygame.locals import *

import random
import math
import time
import enum

from utils import GameFonts, CommonGui, GameInput, GameEvent

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



def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Our Game")
    pygame_flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((0,0), pygame_flags)
    # screen = pygame.display.set_mode((640, 360)) #test resolution
    clock = pygame.time.Clock()

    scr_width = screen.get_width()
    scr_height = screen.get_height()
    print("Screen dimensions ", scr_width, "x", scr_height)
    
    # === TUNABLE SETTINGS ===


    game_scene = "start_screen"
    fonts = GameFonts(screen)
    common_gui = CommonGui(screen)
    

    running = True
    mouse_hold_down = False
    last_frame_time = time.perf_counter()

    gameplay = Gameplay.Gameplay(screen)


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

            if event.type == GameEvent.StartGame:
                game_scene = "playing"
                gameplay.on_game_start(screen, time.perf_counter())

                
            if event.type == GameEvent.GameOver:
                game_scene = "end_screen"


        game_input = GameInput(mousex, mousey, mouse_hold_down, mouse_click_down)

        # === GAME LOGIC and RENDER ===
        # clear display
        screen.fill((255, 255, 255))
        
        
        if game_scene == "start_screen":
            start_screen.start_screen(screen, game_input, fonts, common_gui)
        
        elif game_scene == "playing":
            gameplay.playing(screen, game_input, fonts, common_gui, time.perf_counter())

        elif game_scene == "end_screen":
            end_screen.end_screen(screen, game_input, fonts, common_gui)



        # Time
        now = time.perf_counter()
        frame_duration_in_ms = (now - last_frame_time) * 1000
        last_frame_time = now

        # Display debug info
        frame_duration_display = fonts.debug.render('Frame dur: ' + str(int(frame_duration_in_ms)), False, (0, 0, 0))
        screen.blit(frame_duration_display,(0,screen.get_height() - fonts.debug.size("")[1]))



        pygame.display.flip()


        # limit frames per second
        clock.tick(60)


        
if __name__=="__main__":
    main()