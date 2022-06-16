import pygame
from pygame.locals import *
import random
import math
import WordGenerator
import Letter

"""
TODO:
- detect when letter player has moved is no longer part of a word and whether the word is still valid
- detect when player has added a letter to a word that makes it valid
    - only react when the word makes a valid word? otherwise treat it as if it is just an extra gray letter?
- have letters randomly move away (also determine whether new word is valid)
- different colored words? or different colored letters (by letter)
- custom cursor?
"""

def main():
    pygame.init()
    # create a surface on screen that has the size of the computer screen
    pygame.display.set_caption("Our Game")
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((640, 360)) #test resolution
    clock = pygame.time.Clock()

    scr_width = screen.get_width()
    scr_height = screen.get_height()
    print("Screen dimensions ", scr_width, "x", scr_height)
    
    # === TUNABLE SETTINGS ===
    font_size = int(min(scr_width, scr_height) / 10)
    Letter.font_size=font_size
    # print("Font size: ", font_size)
    font_spacing = int(0.5 * font_size)  #TODO: make this use internal font spacing
    drag_threshold = 0.5 * font_size
    
    generator=WordGenerator.WordGenerator("wordlist.txt")
    words_raw = generator.get_random_word_list(10)
    # words = sorted(words_raw, key=len, reverse=True)

    letters=[]
    #letters_hover=[]
    #rectangles=[]
    words=[] #2D array with arrays that hold the letters in each word -  does it make more sense to keep a list like this, or recalculate it each time?
            
    for word in words_raw:
        legal_pos=False
        num_tries=0
        while not legal_pos and num_tries<500:
            xpos = random.randint(font_size, screen.get_width() - len(word) * font_spacing)
            ypos = random.randint(font_size, screen.get_height() - font_size)
            num_tries=num_tries+1
            legal_pos=True
            possible_word_rect = Rect(xpos-(font_size), ypos-(font_size), (font_spacing*len(word))+(font_size*1.5), font_size*2)
            for letter in letters:
                if letter.rect.colliderect(possible_word_rect):
                    legal_pos=False
        if not legal_pos:
            print("timed out")            
        # print(word, screen.get_width() - len(word) * font_spacing, screen.get_height() - font_size)

        lets_in_word=[]
        for letter in word:
            new_let=Letter.Letter(letter, xpos, ypos)
            lets_in_word.append(new_let)
            letters.append(new_let)
            '''newText=font1.render(letter, True, (100, 100, 100))
            newText_hover = font1.render(letter, True, (25, 25, 25))
            newRect=newText.get_rect()
            # newRect.center=(xpos, ypos + int(0.1 * random.randint(-font_size, font_size)))
            newRect.center=(xpos, ypos)
            letters.append(newText)
            lets_in_word.append(newText)
            letters_hover.append(newText_hover)
            rectangles.append(newRect)'''
            xpos += font_spacing
        words.append(lets_in_word)
                    
    
    running = True
    mouse_hold_down = False

    # -1 if not dragging/hovering over anything, otherwise the id of the rect in the list
    drag_rect_id = -1 
    hover_rect_id = -1

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

        # === GAME LOGIC and RENDER ===
        # clear display
        screen.fill((255, 255, 255))

        if not mouse_hold_down:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            drag_rect_id = -1 #drag nothing

            hover_rect_id = -1
            nearest_rect = (-1, 0) # (rect id, distance from mouse)
            for i in range(0, len(letters)):
                rect = letters[i].rect
                dist = math.hypot(rect.center[0] - mousex, rect.center[1] - mousey)
                # print(i, "distance", dist)
                if dist < nearest_rect[1] or nearest_rect[0] == -1:
                    nearest_rect = (i, dist)
            # print("mouse down nearest rect", nearest_rect)
            # print(words[nearest_rect[0]])
            if nearest_rect[1] < drag_threshold:
                hover_rect_id = nearest_rect[0]

        if mouse_click_down and hover_rect_id != -1:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            drag_rect_id = hover_rect_id
            
        for i in range(0, len(letters)):
            rect = letters[i].rect
            # if rect.collidepoint(mousex, mousey) and mouse_click_down:
            #     drag_rect_id = i

            if i == drag_rect_id:
                rect.update(mousex - 0.5*rect.width, mousey - 0.5*rect.height, rect.width, rect.height)

        for i in range(0, len(letters)):
            # for x in range(0, len(letters)):
                # if x!=i and letters[x].isAdjacentTo(letters[i]):
                    # print(letters[x].char," ",letters[i].char)
            if i == hover_rect_id:
                screen.blit(letters[i].text_hover, letters[i].rect)
            else:
                screen.blit(letters[i].text, letters[i].rect)
                
        pygame.display.flip()

        # limit frames per second
        clock.tick(60)

if __name__=="__main__":
    main()