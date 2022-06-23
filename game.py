import pygame
from pygame.locals import *
import random
import math
import time
import WordGenerator
import Letter

"""
TO DO
-use scrabble distribution when determining which letters to change into
-problem: it is the letters that are part of words that change, and so we end up losing all our vowels
-when to add words to list? each time one is formed or when timer runs out (current method)
-should letters also need to be above letters they come before, the way they need to be to their left?
-actual "you lose" message and option to play again
-more languages
-special abilities when you form certain words (palindromes, >5 letters, etc): choose any letter, slow down time, hint, etc


What is causing it to be so slow?
-two recursive methods (calculate_all_adjacent_strings() and get_best_combo)?
-determining color for each letter?
"""

def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
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

    SHORTEST_ALLOWED_WORD_LENGTH = 2
    
    generator=WordGenerator.WordGenerator("wordlist.txt", SHORTEST_ALLOWED_WORD_LENGTH)
    #words_raw = generator.get_random_word_list(2)
    
    #Debug tools
    debug_font_size = int(min(scr_width, scr_height) / 30)
    debug_font = pygame.font.SysFont('freesanbold.ttf', debug_font_size)
    
    words_used=[]
    
    #available_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (127, 127, 0), (127, 0, 127), (0, 127, 127)]
    available_colors = [(255, 72, 72), (72, 255, 72), (72, 72, 255), (255, 72, 255), (72, 255, 255), (255, 72, 0)]

    letters=[]
    chars=generator.get_random_chars(25)
    
    for char in chars:
        new_let=Letter.Letter(char, 0, 0)
        legal_pos=False
        while not legal_pos:
            xpos = random.randint(font_size, screen.get_width() - font_spacing)
            ypos = random.randint(font_size, screen.get_height() - font_size)
            new_let.rect.center=(xpos, ypos)
            legal_pos=True
            for let in letters:
                if let.isAdjacentAndLeft(new_let) or new_let.isAdjacentAndLeft(let):
                    legal_pos=False
                    break
                    
        letters.append(new_let)

    running = True
    mouse_hold_down = False
    
    # -1 if not dragging/hovering over anything, otherwise the id of the rect in the list
    drag_rect = None
    hover_rect = None

    time_between_explosions = 20 #seconds
    last_explosion = time.perf_counter()

    last_frame_word_combo = []

    last_frame_time = time.perf_counter()

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
            drag_rect = None #drag nothing

            hover_rect = None
            nearest_rect = (None, 0) # (rect id, distance from mouse)
            for let in letters:
                (x, y) = let.coords()
                dist = math.hypot(x - mousex, y - mousey)
                # print(i, "distance", dist)
                if dist < nearest_rect[1] or nearest_rect[0] == None:
                    nearest_rect = (let.rect, dist)
            # print("mouse down nearest rect", nearest_rect)
            # print(words[nearest_rect[0]])
            if nearest_rect[1] < drag_threshold:
                hover_rect = nearest_rect[0]

        if mouse_click_down and hover_rect != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            drag_rect = hover_rect

        # Update the dragged letter's pos, if we are dragging
        if drag_rect != None:
            drag_rect.update(mousex - 0.5*drag_rect.width, mousey - 0.5*drag_rect.height, drag_rect.width, drag_rect.height)

        # Time
        now = time.perf_counter()
        frame_duration_in_ms = (now - last_frame_time) * 1000
        last_frame_time = now

        #Explosion        
        explosion_relative_time_left = 1 - (now - last_explosion) / time_between_explosions
        if now - last_explosion > time_between_explosions:
            last_explosion = now
            time_between_explosions = 0.9 * time_between_explosions

            # Stop the game if there are no more words to explode
            if len(last_frame_word_combo) == 0:
                print("YOU LOSE")
                return
            
            word_to_explode = last_frame_word_combo[0]
            # pick a letter to explode, excluding both endpoint letters
            letter_num = 0
            if len(word_to_explode) < 3:
                letter_num = random.randint(0,1)
            else:
                letter_num = random.randint(1, len(word_to_explode) - 1)

            letter = word_to_explode[letter_num]
            previous_char = letter.char
            choice_alphabet = alphabet.replace(previous_char, "")   # base this on scrabble distribution in WordGenerator instead
            assert len(choice_alphabet) == 25
            new_char = random.choice(choice_alphabet)
            new_letter = Letter.Letter(new_char, letter.coords()[0], letter.coords()[1])

            letters[letters.index(letter)] = new_letter
            
            #update words used
            for word in last_frame_word_combo:
                word_raw=""
                for let in word:
                    word_raw+=let.char
                if not word_raw in words_used:
                    words_used.append(word_raw)
                    generator.remove_word(word_raw)

            # xpos = random.randint(font_size, screen.get_width() - font_size)
            # ypos = random.randint(font_size, screen.get_height() - font_size)
            # word_to_explode[letter_num].rect.center = (xpos, ypos)


            # Explode a whole word
            # for letter_to_explode in word_to_explode:
            #     xpos = random.randint(font_size, screen.get_width() - font_size)
            #     ypos = random.randint(font_size, screen.get_height() - font_size)
            #     letter_to_explode.rect.center = (xpos, ypos)

        
        start = time.perf_counter_ns()

        connected_letters = []
        for i in range(0, len(letters)):
 
            my_connected_letters = []
            for j in range(0, len(letters)):
                if j == i:
                    pass
                else:
                    if letters[i].isAdjacentAndLeft(letters[j]):
                        my_connected_letters.append(j)
            connected_letters.append(my_connected_letters)

        step1 = time.perf_counter_ns()

        all_possible_strings = []
        for letter_id in range(0, len(letters)):
            possible_strings = calculate_all_adjacent_strings(connected_letters, letter_id, [], "")
            for pos_str in possible_strings:
                all_possible_strings.append(pos_str)

    
        step2= time.perf_counter_ns()

        possible_words = []
        possible_words_raw = []
        for i in range(0, len(all_possible_strings)):
            string_ids = all_possible_strings[i]
            my_str = ""
            for index in string_ids:
                my_str += letters[index].char

            if generator.is_valid_word(my_str):
                letters_in_word = map(lambda let_id: letters[let_id], string_ids)
                possible_words.append(list(letters_in_word))
                possible_words_raw.append(my_str)


        step3 = time.perf_counter_ns()
        
        word_combo=get_best_combo([], possible_words)
        last_frame_word_combo = word_combo
        
        words_raw=""
        for word in word_combo:
            for let in word:
                words_raw+=let.char
            words_raw+=", "
        #print(words_raw)
            
        
        end = time.perf_counter_ns()

        """
        print(connected_letters)
        print("\n")
        # print(all_possible_strings)
        # print(all_strs)
        # print(possible_words)
        print(possible_words_raw)
        print(w)
        print("Took", (end-start) / 1_000_000, "ms")
        print("Step1 took", (step1-start) / 1_000_000, "ms")
        print("Step2 took", (step2-step1) / 1_000_000, "ms")
        print("Step3 took", (step3-step2) / 1_000_000, "ms")
        print("Step4 took", (now-step3) / 1_000_000, "ms")
        """
                        
        strings=""
        for let in unused_letters_in_combo(word_combo, letters):
            strings+=let.char+", "
            let.connected=False
        #print(strings)
        
        #add colors back in to available_colors if no connected letters are already using them
        for let in letters:
            if not let.color in available_colors:
                available=True
                for let2 in letters:
                    if let2!=let and let2.color==let.color and let2.connected==True:
                        available=False
                if available:
                    available_colors.append(let.color)
                            
        #Blit word connections to screen
        for word in word_combo:
            color=(100, 100, 100)
            for i in range(0, len(word)-1):
                left_letter = word[i]
                right_letter = word[i+1]

                pygame.draw.line(screen, (0,0,0), left_letter.coords(), right_letter.coords(), 3)
                
                if (left_letter.color in available_colors or left_letter.connected==True) and left_letter.color!=(100, 100, 100):
                    color=left_letter.color
                    
                if left_letter.connected==False:
                    left_letter.connected=True
                    
            if word[len(word)-1].connected==False: # check this one because loop only goes to len(word)-1 and it was skipped
                word[len(word)-1].connected=True
                                        
            if color==(100, 100, 100):
                if len(available_colors)>0:
                    color=random.choice(available_colors)
                else:
                    color=word[0].color
            if color in available_colors:
                available_colors.remove(color)
            for let in word:
                let.color=color
        
        # Blit the letters to screen
        for i in range(0, len(letters)):
            screen.blit(letters[i].generate_font(), letters[i].rect)
            
        # Blit the explosion timer to screen
        explosion_candle_rect = Rect(0,0, explosion_relative_time_left * scr_width, 0.025*scr_height)
        pygame.draw.rect(screen, (0,0,255), explosion_candle_rect)
        
        # Blit words used to screen
        ycoord=explosion_candle_rect.height+5
        words_used_header = debug_font.render("Words Used", False, (0, 0, 0))
        screen.blit(words_used_header, (5, ycoord))
        for word in words_used:
            word_txt = debug_font.render(word, False, (0, 0, 0))
            ycoord+=debug_font.get_height()
            screen.blit(word_txt, (5, ycoord))

        # Display debug info
        frame_duration_display = debug_font.render('Frame dur: ' + str(int(frame_duration_in_ms)), False, (0, 0, 0))
        screen.blit(frame_duration_display,(0,scr_height - debug_font_size))

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
    best_combo=words_in_combo
    for word in possible_words:
        if not word in words_in_combo:#check for repeat word since we don't remove words from possible_words when used
            repeat_letter=False
            for w in words_in_combo:
                for let in w:
                    if let in word:
                        repeat_letter=True
                        break
                if repeat_letter==True:
                    break
            if repeat_letter==False:
                temp=words_in_combo.copy()
                temp.append(word)
                best_combo_this_route=get_best_combo(temp, possible_words)
                possible_letters=[]
                for w in possible_words:
                    possible_letters=possible_letters+w
                best_combo_this_route_unused=len(unused_letters_in_combo(best_combo_this_route, possible_letters))
                best_combo_unused=len(unused_letters_in_combo(best_combo, possible_letters))
                if best_combo_this_route_unused<best_combo_unused:
                    best_combo=best_combo_this_route
                elif best_combo_this_route_unused==best_combo_unused and len(best_combo_this_route)<len(best_combo):
                        best_combo=best_combo_this_route
    return best_combo
        
def unused_letters_in_combo(combo, possible_letters):
    combo_lets=[]
    unused=[]
    for let in possible_letters:
        present=False
        for word in combo:
            if let in word:
                present=True
                break
        if not present:
            unused.append(let)
    return unused
        
if __name__=="__main__":
    main()