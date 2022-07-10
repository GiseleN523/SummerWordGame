import pygame
from pygame import Rect

import math
import random
import time


from utils import GameEvent
import WordGenerator
import Letter


SHORTEST_ALLOWED_WORD_LENGTH = 2
ALL_COLORS = [(255, 72, 72), (72, 255, 72), (72, 72, 255), (255, 72, 255), (72, 255, 255), (255, 72, 0)]

STARTING_TIME_BETWEEN_EXPLOSIONS = 5 #20 #seconds

DRAG_THRESHOLD_MOD = 0.5


class Gameplay:


    def __init__(self, screen):
        self.word_generator= WordGenerator.WordGenerator("wordlist.txt", SHORTEST_ALLOWED_WORD_LENGTH)


    def on_game_start(self, screen, game_time):
        self.words_used=[]
        self.available_colors = ALL_COLORS

        # None if not dragging/hovering over anything, otherwise the id of the rect in the list
        self.drag_rect = None
        self.hover_rect = None

        self.time_between_explosions= STARTING_TIME_BETWEEN_EXPLOSIONS
        self.last_explosion = game_time


        self.last_frame_word_combo = []

        self.letter_radius = int(min(screen.get_width(), screen.get_height()) / 10)


        starting_letters = self.word_generator.get_random_chars(25)
        self.letters= create_letters(starting_letters, screen.get_width(), screen.get_height(), self.letter_radius)




    def playing(self, screen, game_input, fonts, common_gui, game_time):

        if not game_input.mouse_hold_down:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.drag_rect = None #drag nothing

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

            drag_threshold = DRAG_THRESHOLD_MOD * self.letter_radius

            if nearest_rect[1] < drag_threshold:
                self.hover_rect = nearest_rect[0]

        if game_input.mouse_click_down and self.hover_rect != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.drag_rect = self.hover_rect

        # Update the dragged letter's pos, if we are dragging
        if self.drag_rect != None:
            self.drag_rect.update(game_input.mouse_x - 0.5*self.drag_rect.width, game_input.mouse_y - 0.5*self.drag_rect.height, self.drag_rect.width, self.drag_rect.height)


        #Explosion
        explosion_relative_time_left = 1 - (game_time - self.last_explosion) / self.time_between_explosions
        if game_time - self.last_explosion > self.time_between_explosions:
            self.last_explosion = game_time
            self.time_between_explosions = 0.9 * self.time_between_explosions


            # Stop the game if there are no more words to explode
            if len(self.last_frame_word_combo) == 0:
                pygame.event.post(pygame.event.Event(GameEvent.GameOver))
                return
            
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
            new_letter = Letter.Letter(new_char, letter.coords()[0], letter.coords()[1], self.letter_radius)

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

        connected_letters = generate_connection_graph(self.letters)

        step1 = time.perf_counter_ns()




        step2= time.perf_counter_ns()


        possible_words = calculate_all_possible_words_from_graph(self.letters, connected_letters, self.word_generator)


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
            







def create_letters(chars, screen_width, screen_height, letter_radius):
    letters=[]
    for char in chars:
        new_let=Letter.Letter(char, 0, 0, letter_radius)
        legal_pos=False
        while not legal_pos:
            # TODO: also make sure letter doesn't intersect word list on left
            xpos = random.randint(letter_radius, screen_width - letter_radius)
            ypos = random.randint(letter_radius, screen_height - letter_radius)
            new_let.rect.center=(xpos, ypos)
            legal_pos=True
            for let in letters:
                if let.isAdjacentAndLeft(new_let) or new_let.isAdjacentAndLeft(let):
                    legal_pos=False
                    break         
        letters.append(new_let)
    return letters



def string_from_letter_indices(letters, indices):
    return ''.join(list(map(lambda id: letters[id].char, indices)))



def generate_connection_graph(letters):
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

    return connected_letters


def calculate_all_possible_words_from_graph(letters, connected_letters, word_generator):

    possible_words = []
    for letter in letters:
        new_words = calculate_all_adjacent_strings(connected_letters, 0, [], letters, word_generator)

        possible_words.extend(new_words)

    return possible_words


def calculate_all_adjacent_strings(connection_graph, starting_point, visited, letters, word_generator):
    results = []
    visited.append(starting_point)

    # If we don't traverse the graph any further, what we have is still a string
    snippet_base = string_from_letter_indices(letters, visited)

    if word_generator.is_valid_word(snippet_base):
        results.append(visited.copy())

    # A list of all letters (as int ids) that I connect to
    connections = connection_graph[starting_point]

    valid_connections = []
    # snippet_base = ''.join(list(map(lambda id: letters[id].char, visited)))
    # print(snippet_base)

    for connection in connections:
        if connection not in visited:

            snippet = snippet_base + letters[connection].char
            if word_generator.is_valid_word_front_snippet(snippet):

                new_results = calculate_all_adjacent_strings(connection_graph, connection, visited, letters, word_generator)
                for new_result in new_results:
                    results.append(new_result)

    # Remove the last element of the list, presumably me
    visited.pop(-1)

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




def test_word_finder_performance():

    setup_start = time.perf_counter_ns()

    # Mock setup
    pygame.init()
    word_generator= WordGenerator.WordGenerator("wordlist.txt", SHORTEST_ALLOWED_WORD_LENGTH)

    setup_end = time.perf_counter_ns()

    # print("Took", int((setup_end - setup_start) / 1_000_000), "ms to setup test")


    letters = []
    for i in range(0, 2):
        word = random.choice(list(word_generator.word_map.keys()))
        print(word)
        offset = 0
        for letter in word:
            letters.append(Letter.Letter(letter, offset, i*9, 10))
            offset += 5

    # print(letters)

    start = time.perf_counter_ns()

    connected_letters = generate_connection_graph(letters)
    # print("Connection graph", connected_letters)

    graph_complete = time.perf_counter_ns()


    possible_words = calculate_all_possible_words_from_graph(letters, connected_letters, word_generator)

    # [print(string_from_letter_indices(letters, my_str)) for my_str in possible_words]
    
    possible_words_complete = time.perf_counter_ns()
    
    word_combo = get_best_combo([], possible_words)

    end = time.perf_counter_ns()

    total_duration = end  - start
    graph_duration = graph_complete - start
    possible_words_duration = possible_words_complete - graph_complete
    word_combo_duration = end - possible_words_complete

    print(word_combo)

    print("Total time      ", int(total_duration / 1_000_000), "ms")
    print("Connection graph", int(graph_duration / 1_000_000), "ms")
    print("Possible words  ", int(possible_words_duration / 1_000_000), "ms")
    print("Word combo      ", int(word_combo_duration / 1_000_000), "ms")


# For testing purposes
if __name__=="__main__":
    test_word_finder_performance()
    