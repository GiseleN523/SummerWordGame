import random
import math

def getRandomWordList(num_words, min_length, max_length):
    file=open("wordlist.txt", "r") # read file
    word_list=file.readlines()
    for i in range(0, len(word_list)):
        word_list[i]=word_list[i].replace("\n", "")
        
    randomWordList=[]
    letter_counts_dict=getScrabbleDistributionFor(num_words, min_length, max_length)
    for x in range(0, num_words):
        legal_word=False
        while not legal_word:
            legal_word=True
            word=random.choice(word_list)
            # print(word)
            if len(word)<min_length or len(word)>max_length:
                legal_word=False
            for char in word:
                char=char.lower()
                if char in letter_counts_dict and letter_counts_dict[char]<=0:
                    legal_word=False
        randomWordList.append(word)
        for char in word:
            char=char.lower()
            if char in letter_counts_dict:
                letter_counts_dict[char]=letter_counts_dict[char]+1
        # print(letter_counts_dict)
    return randomWordList

def getScrabbleDistributionFor(num_words, min_length, max_length):
    max_possible_letters=num_words*max_length
    ratio=max_possible_letters/100  # there are 100 letters in scrabble
    # print(ratio)
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
    # print(letter_counts_dict)
    return letter_counts_dict

def main():
    print(getRandomWordList(3, 0, 5))

if __name__=="__main__":
    main()