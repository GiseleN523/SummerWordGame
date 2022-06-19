import pygame
from pygame.locals import *
import random
import math
import time
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
    words_raw = generator.get_random_word_list(1)

    total_num_letters=0
    for word in words_raw:
        total_num_letters=total_num_letters+len(word)

    # words = sorted(words_raw, key=len, reverse=True)

    letters=[]
    #letters_hover=[]
    #rectangles=[]
    words=[] #2D array with arrays that hold the letters in each word -  does it make more sense to keep a list like this, or recalculate it each time?
            

    current_word_id = 0

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
            new_let.word_id = current_word_id
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
        current_word_id += 1




    # print(connected_letters)

    
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
                (x, y) = letters[i].coords()
                dist = math.hypot(x - mousex, y - mousey)
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

        # Update the dragged letter's pos, if we are dragging
        if drag_rect_id >= 0:
            rect = letters[drag_rect_id].rect
            rect.update(mousex - 0.5*rect.width, mousey - 0.5*rect.height, rect.width, rect.height)

        
        start = time.perf_counter_ns()

        connected_letters = []
        for i in range(0, len(letters)):
 
            my_connected_letters = []
            for j in range(0, len(letters)):
                if j == i:
                    pass
                else:
                    if letters[i].isAdjacentTo(letters[j]):
                        my_connected_letters.append(j)
                        # if not j in connected_letters:
                            # connected_letters.append(j)
            connected_letters.append(my_connected_letters)

        step1 = time.perf_counter_ns()

        all_possible_strings = []
        for letter_id in range(0, len(letters)):
            possible_strings = calculate_all_adjacent_strings(connected_letters, letter_id, [], "")
            for pos_str in possible_strings:
                all_possible_strings.append(pos_str)
        

        step2= time.perf_counter_ns()

        # all_strs = []
        # for string_ids in all_possible_strings:
        #     my_str = ""
        #     for id in string_ids:
        #         my_str += letters[id].char
        #     all_strs.append(my_str)

        possible_words = []
        possible_words_raw = []
        for i in range(0, len(all_possible_strings)):
            string_ids = all_possible_strings[i]
            my_str = ""
            for index in string_ids:
                my_str += letters[index].char

            #Do we want a lower letter bound for valid words?
            if generator.is_valid_word(my_str):
                letters_in_word = map(lambda let_id: letters[let_id], string_ids)
                possible_words.append(list(letters_in_word))
                possible_words_raw.append(my_str)


        step3 = time.perf_counter_ns()

        # word_combo=get_best_combo([], possible_words)
        

        end = time.perf_counter_ns()

        print(connected_letters)
        print("\n")

        # print(all_possible_strings)
        # print(all_strs)
        # print(possible_words)
        print(possible_words_raw)
        print("Took", (end-start) / 1_000_000, "ms")
        print("Step1 took", (step1-start) / 1_000_000, "ms")
        print("Step2 took", (step2-step1) / 1_000_000, "ms")
        print("Step3 took", (step3-step2) / 1_000_000, "ms")
        print("Step4 took", (end-step3) / 1_000_000, "ms")




        return

        possible_words=[]
        for adjacent_letters in connected_letters:
            for adj_letter in adjacent_letters:
                word="hello"
                '''some logic to traverse graph'''
                if generator.is_valid_word(word):
                    possible_words.append(word)

        word_combo=get_best_combo([], possible_words)
        
        # Blit the letters to screen
        for i in range(0, len(letters)):
            if i == hover_rect_id:
                screen.blit(letters[i].text_hover, letters[i].rect)
            # if i in connected_letters:
            #     screen.blit(letters[i].text_red, letters[i].rect)
            else:
                word_id = letters[i].word_id
                screen.blit(letters[i].with_color(word_id), letters[i].rect)

            # for x in range(0, len(letters)):
                # if x!=i and letters[x].isAdjacentTo(letters[i]):
                    # print(letters[x].char," ",letters[i].char)
                
        pygame.display.flip()

        # limit frames per second
        clock.tick(60)

def calculate_all_adjacent_strings(connection_graph, starting_point, visited, tab):
    results = []
    visited.append(starting_point)

    #We also append shorter strings
    results.append(visited.copy())

    connections = connection_graph[starting_point]

    valid_connections = []
    invalid = []
    for con in connections:
        if not con in visited:
            valid_connections.append(con)
        else:
            invalid.append(con)

    # print(tab, starting_point, valid_connections, "        but not:", invalid)
    new_tab = tab + " |"

    if len(valid_connections) == 0:
        #turn around
        pass
    else:
        for letter_id in valid_connections:
            new_results = calculate_all_adjacent_strings(connection_graph, letter_id, visited, new_tab)
            for new_result in new_results:
                results.append(new_result)
            # print(tab, starting_point, letter_id)

    visited.remove(starting_point)
    return results
    


def get_best_combo(words_in_combo, possible_words):
    print(words_in_combo)
    print("it")
    best_combo=words_in_combo
    for word in possible_words:

        if not word in words_in_combo:#check for repeat word since we don't remove words from possible_words when used
            repeat_letter=False
            for w in words_in_combo:
                for let in w:
                    if word.contains(let):
                        repeat_letter=True
            if repeat_letter==False:
                best_combo_this_route=get_best_combo(words_in_combo.append(word), possible_words)
                if num_unused_letters_in_combo(best_combo_this_route, possible_words)>num_unused_letters_in_combo(best_combo, possible_words):
                    best_combo=best_combo_this_route
    return best_combo
        
def num_unused_letters_in_combo(words, total_num_letters):
    lets_in_combo=0
    for word in words:
        lets_in_combo=lets_in_combo+len(word)
    return total_num_letters-lets_in_combo

if __name__=="__main__":
    main()