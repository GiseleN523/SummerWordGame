import pygame
from pygame import Rect

import math
import random
import time


import WordGenerator
import Letter


SHORTEST_ALLOWED_WORD_LENGTH = 2
ALL_COLORS = [(255, 72, 72), (72, 255, 72), (72, 72, 255), (255, 72, 255), (72, 255, 255), (255, 72, 0)]

STARTING_TIME_BETWEEN_EXPLOSIONS = 5 #20 #seconds


class Gameplay:


    def __init__(self):
        self.word_generator= WordGenerator.WordGenerator("wordlist.txt", SHORTEST_ALLOWED_WORD_LENGTH)


    def on_game_start(self, screen):
        self.words_used=[]

        self.letters= create_letters(self.word_generator.get_random_chars(25), screen)
        self.available_colors = ALL_COLORS

        # None if not dragging/hovering over anything, otherwise the id of the rect in the list
        self.drag_rect = None
        self.hover_rect = None

        self.drag_threshold = 0.5 * Letter.font_size

        self.time_between_explosions= STARTING_TIME_BETWEEN_EXPLOSIONS
        self.last_explosion = time.perf_counter()

        self.last_frame_word_combo = []

        self.last_frame_time = time.perf_counter()




    def playing(self, screen, game_input, fonts, common_gui):

        if not game_input.mouse_hold_down:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            drag_rect = None #drag nothing

            self.hover_rect = None
            nearest_rect = (None, 0) # (rect id, distance from mouse)
            for let in self.letters:
                (x, y) = let.coords()
                dist = math.hypot(x - game_input.mouse_x, y - game_input.mouse_y)
                # print(i, "distance", dist)
                if dist < nearest_rect[1] or nearest_rect[0] == None:
                    nearest_rect = (let.rect, dist)
            # print("mouse down nearest rect", nearest_rect)
            # print(words[nearest_rect[0]])
            if nearest_rect[1] < self.drag_threshold:
                self.hover_rect = nearest_rect[0]

        if game_input.mouse_click_down and self.hover_rect != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.drag_rect = self.hover_rect

        # Update the dragged letter's pos, if we are dragging
        if self.drag_rect != None:
            self.drag_rect.update(game_input.mouse_x - 0.5*self.drag_rect.width, game_input.mouse_y - 0.5*self.drag_rect.height, self.drag_rect.width, self.drag_rect.height)

        # Time
        now = time.perf_counter()
        frame_duration_in_ms = (now - self.last_frame_time) * 1000
        self.last_frame_time = now

        #Explosion        
        explosion_relative_time_left = 1 - (now - self.last_explosion) / self.time_between_explosions
        if now - self.last_explosion > self.time_between_explosions:
            self.last_explosion = now
            self.time_between_explosions = 0.9 * self.time_between_explosions

            # Stop the game if there are no more words to explode
            if len(self.last_frame_word_combo) == 0:
                return True #Yes, move to end screen
            
            word_to_explode = self.last_frame_word_combo[0]
            # pick a letter to explode, excluding both endpoint letters
            letter_num = 0
            if len(word_to_explode) < 3:
                letter_num = random.randint(0,1)
            else:
                letter_num = random.randint(1, len(word_to_explode) - 1)

            letter = word_to_explode[letter_num]
            previous_char = letter.char
            #choice_alphabet = alphabet.replace(previous_char, "")   # base this on scrabble distribution in WordGenerator instead
            #assert len(choice_alphabet) == 25
            #new_char = random.choice(choice_alphabet)
            existing_chars=[]
            for let in self.letters:
                existing_chars.append(let.char)
            new_char= self.word_generator.get_random_chars(1, existing_chars)[0]
            new_letter = Letter.Letter(new_char, letter.coords()[0], letter.coords()[1])

            self.letters[self.letters.index(letter)] = new_letter
            
            #update words used
            for word in self.last_frame_word_combo:
                word_raw=""
                for let in word:
                    word_raw+=let.char
                if not word_raw in self.words_used:
                    self.words_used.append(word_raw)
                    self.word_generator.remove_word(word_raw)

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
        for i in range(0, len(self.letters)):

            my_connected_letters = []
            for j in range(0, len(self.letters)):
                if j == i:
                    pass
                else:
                    if self.letters[i].isAdjacentAndLeft(self.letters[j]):
                        my_connected_letters.append(j)
            connected_letters.append(my_connected_letters)

        step1 = time.perf_counter_ns()

        all_possible_strings = []
        for letter_id in range(0, len(self.letters)):
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
                my_str += self.letters[index].char

            if self.word_generator.is_valid_word(my_str):
                letters_in_word = map(lambda let_id: self.letters[let_id], string_ids)
                possible_words.append(list(letters_in_word))
                possible_words_raw.append(my_str)


        step3 = time.perf_counter_ns()
        
        word_combo = get_best_combo([], possible_words)
        self.last_frame_word_combo = word_combo
        
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
        for let in unused_letters_in_combo(word_combo, self.letters):
            strings+=let.char+", "
            let.connected=False
        #print(strings)
        
        #add colors back in to available_colors if no connected letters are already using them
        for let in self.letters:
            if not let.color in self.available_colors:
                available=True
                for let2 in self.letters:
                    if let2!=let and let2.color==let.color and let2.connected==True:
                        available=False
                if available:
                    self.available_colors.append(let.color)
                            
        #Blit word connections to screen
        for word in word_combo:
            color=(100, 100, 100)
            for i in range(0, len(word)-1):
                left_letter = word[i]
                right_letter = word[i+1]

                pygame.draw.line(screen, (0,0,0), left_letter.coords(), right_letter.coords(), 3)
                
                if (left_letter.color in self.available_colors or left_letter.connected==True) and left_letter.color!=(100, 100, 100):
                    color=left_letter.color
                    
                if left_letter.connected==False:
                    left_letter.connected=True
                    
            if word[len(word)-1].connected==False: # check this one because loop only goes to len(word)-1 and it was skipped
                word[len(word)-1].connected=True
                                        
            if color==(100, 100, 100):
                if len(self.available_colors)>0:
                    color=random.choice(self.available_colors)
                else:
                    color=word[0].color
            if color in self.available_colors:
                self.available_colors.remove(color)
            for let in word:
                let.color=color
        
        # Blit the letters to screen
        for i in range(0, len(self.letters)):
            screen.blit(self.letters[i].generate_font(), self.letters[i].rect)
            
        # Blit the explosion timer to screen
        explosion_candle_rect = Rect(0,0, explosion_relative_time_left * screen.get_width(), 0.025* screen.get_height())
        pygame.draw.rect(screen, (0,0,255), explosion_candle_rect)
        
        # Blit words used to screen
        ycoord=explosion_candle_rect.height+5
        words_used_header = fonts.debug.render("Words Used", False, (0, 0, 0))
        screen.blit(words_used_header, (5, ycoord))
        for word in self.words_used:
            word_txt = fonts.debug.render(word, False, (0, 0, 0))
            ycoord+=fonts.debug.get_height()
            screen.blit(word_txt, (5, ycoord))
            
        # Display debug info
        frame_duration_display = fonts.debug.render('Frame dur: ' + str(int(frame_duration_in_ms)), False, (0, 0, 0))
        screen.blit(frame_duration_display,(0,screen.get_height() - fonts.debug.size("")[1]))

        return False



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


def create_letters(chars, screen):
    letters=[]
    for char in chars:
        new_let=Letter.Letter(char, 0, 0)
        legal_pos=False
        while not legal_pos:
            xpos = random.randint(Letter.font_size, screen.get_width() - Letter.font_size)
            ypos = random.randint(Letter.font_size, screen.get_height() - Letter.font_size) # to do: also make sure letter doesn't intersect word list on left
            new_let.rect.center=(xpos, ypos)
            legal_pos=True
            for let in letters:
                if let.isAdjacentAndLeft(new_let) or new_let.isAdjacentAndLeft(let):
                    legal_pos=False
                    break         
        letters.append(new_let)
    return letters

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
                best_combo_this_route= get_best_combo(temp, possible_words)
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