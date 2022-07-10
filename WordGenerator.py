import random
import math
import time

class WordGenerator:
    def __init__(self, filename, shortest_allowed_word_length):

        # start_time = time.perf_counter_ns()

        file=open(filename, "r") # read file
        self.shortest_allowed_word_length = shortest_allowed_word_length

        word_list=file.readlines()

        self.word_map = {}

        # Holds keys to all word snippets that exist where the snippet must
        # start at the beginning of the word
        # Used to filter out strings as non-words
        self.word_snippet_map = {}

        for w in word_list:
            word=w.replace("\n", "").upper()
            if len(word)>=self.shortest_allowed_word_length:
                #the value of the dictionary doesn't matter, only the existence of the key                
                self.word_map[word] = True 

                snippet = ""
                for letter in word:
                    snippet += letter
                    self.word_snippet_map[snippet] = True

        # end_time = time.perf_counter_ns()

        # print("Took", int( (end_time - start_time) / 1_000_000), "ms to create word hashmaps")

        # print(len(self.word_snippet_map))
        

    def longest_word_len(self):
        longest_word=""
        for word in self.word_map:
            if len(word)>len(longest_word):
                longest_word=word
        return len(longest_word)

    def is_valid_word(self, word):
        return word in self.word_map

    def is_valid_word_front_snippet(self, snippet):
        return snippet in self.word_snippet_map
    
    def remove_word(self, word):
        self.word_map.pop(word)
    
    def get_random_chars(self, num, existing_chars=[]):
        letter_counts_dict=self.get_scrabble_distribution_for(num)
        for char in existing_chars: # only runs if existing_chars argument was passed
            if char in letter_counts_dict:
                letter_counts_dict[char]=letter_counts_dict[char]-1
        chars=[]
        while len(chars)<num:
            char=random.choice(list(letter_counts_dict))
            if char in letter_counts_dict and letter_counts_dict[char]>0:
                chars.append(char)
                letter_counts_dict[char]=letter_counts_dict[char]-1
        return chars

    def get_scrabble_distribution_for(self, num_letters):
        ratio=num_letters/100  # there are 100 letters in scrabble
        letter_counts_dict={
            "A" : math.ceil(9*ratio),
            "B" : math.ceil(2*ratio),
            "C" : math.ceil(2*ratio),
            "D" : math.ceil(4*ratio),
            "E" : math.ceil(12*ratio),
            "F" : math.ceil(2*ratio),
            "G" : math.ceil(3*ratio),
            "H" : math.ceil(2*ratio),
            "I" : math.ceil(9*ratio),
            "J" : math.ceil(1*ratio),
            "K" : math.ceil(1*ratio),
            "L" : math.ceil(4*ratio),
            "M" : math.ceil(2*ratio),
            "N" : math.ceil(6*ratio),
            "O" : math.ceil(8*ratio),
            "P" : math.ceil(2*ratio),
            "Q" : math.ceil(1*ratio),
            "R" : math.ceil(6*ratio),
            "S" : math.ceil(4*ratio),
            "T" : math.ceil(6*ratio),
            "U" : math.ceil(4*ratio),
            "V" : math.ceil(2*ratio),
            "W" : math.ceil(2*ratio),
            "X" : math.ceil(1*ratio),
            "Y" : math.ceil(2*ratio),
            "Z" : math.ceil(1*ratio)
        }
        return letter_counts_dict