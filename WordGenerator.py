import random
import math

class WordGenerator:
    def __init__(self, filename, shortest_allowed_word_length):
        file=open(filename, "r") # read file
        self.shortest_allowed_word_length = shortest_allowed_word_length

        self.word_list=file.readlines()
        for i in range(0, len(self.word_list)):
            self.word_list[i] = self.word_list[i].replace("\n", "")

        #Iterate backwards over list and delete words that are too short
        for i in range(len(self.word_list) - 1, -1, -1):
            if len(self.word_list[i]) < self.shortest_allowed_word_length:
                self.word_list.pop(i)

        self.word_map = {}
        for word in self.word_list:
            self.word_map[word] = True #the value of the dictionary doesn't matter, only the existence of the key

    def longest_word_len(self):
        longest_word=""
        for word in self.word_list:
            if len(word)>len(longest_word):
                longest_word=word
        return len(longest_word)
    
    def is_valid_word(self, word):
        return word in self.word_map
        # for w in self.word_list:
        #     if w.lower()==word.lower():
        #         return True
        # return False
            
    def get_random_word_list(self, num_words, min_length=None, max_length=None): 
        random_word_list=[]
        letter_counts_dict=self.get_scrabble_distribution_for(num_words, max_length)
        for x in range(0, num_words):
            legal_word=False
            while not legal_word:
                legal_word=True
                word=random.choice(self.word_list)
                if min_length is not None and max_length is not None:
                    if len(word)<min_length or len(word)>max_length:
                        legal_word=False
                for char in word:
                    char=char.lower()
                    if char in letter_counts_dict and letter_counts_dict[char]<=0:
                        legal_word=False
            random_word_list.append(word)
            for char in word:
                char=char.lower()
                if char in letter_counts_dict:
                    letter_counts_dict[char]=letter_counts_dict[char]+1
        return random_word_list

    def get_scrabble_distribution_for(self, num_words, max_length):
        if max_length is None:
            max_length=self.longest_word_len()
        max_possible_letters=num_words*max_length
        ratio=max_possible_letters/100  # there are 100 letters in scrabble
        letter_counts_dict={
            "a" : math.ceil(9*ratio),
            "b" : math.ceil(2*ratio),
            "c" : math.ceil(2*ratio),
            "d" : math.ceil(4*ratio),
            "e" : math.ceil(12*ratio),
            "f" : math.ceil(2*ratio),
            "g" : math.ceil(3*ratio),
            "h" : math.ceil(2*ratio),
            "i" : math.ceil(9*ratio),
            "j" : math.ceil(1*ratio),
            "k" : math.ceil(1*ratio),
            "l" : math.ceil(4*ratio),
            "m" : math.ceil(2*ratio),
            "n" : math.ceil(6*ratio),
            "o" : math.ceil(8*ratio),
            "p" : math.ceil(2*ratio),
            "q" : math.ceil(1*ratio),
            "r" : math.ceil(6*ratio),
            "s" : math.ceil(4*ratio),
            "t" : math.ceil(6*ratio),
            "u" : math.ceil(4*ratio),
            "v" : math.ceil(2*ratio),
            "w" : math.ceil(2*ratio),
            "x" : math.ceil(1*ratio),
            "y" : math.ceil(2*ratio),
            "z" : math.ceil(1*ratio)
        }
        return letter_counts_dict
    
    def all_possible_words_for(self, letters):#takes array of strings
        return self.all_possible_words_for_helper("", letters)

def main():
    generator = word_generator("wordlist.txt")
    print(generator.get_random_word_list(3, 0, 5))

if __name__=="__main__":
    main()