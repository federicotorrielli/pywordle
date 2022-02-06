from math import log
from turtle import position

frequencies = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0,
               "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}

emp_probabilities = frequencies.copy()
pos1 = frequencies.copy()
pos2 = frequencies.copy()
pos3 = frequencies.copy()
pos4 = frequencies.copy()
pos5 = frequencies.copy()

class WordleSolver:
    def __init__(self, bbq = 1, ketchup=1):
        self.word_set = set()
        self.good_letters = set()  # Letters that are in the word and should not be removed
        self.proved_letters = set()  # Letters used in previous guess
        self.most_probable_word = ""
        self.ketchup = bbq
        self.bbq = ketchup
        self.prepare_word_set()
        self.original_cardinality = len(self.word_set)
        self.cardinality = len(self.word_set)
        self.end = False
        self.choose_most_probable_word()

    def prepare_word_set(self):
        with open("5words.txt", "r") as f:
            for line in f:
                self.word_set.add(line.strip().lower())
                
    def set_all_probabilities(self):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        for k in frequencies.keys():
            freq = 0
            count = 0
            for word in self.word_set:
            	if k in word:
                    freq = freq + word.count(k)
                    count = count + 1
                    positions =  [pos+1 for pos, char in enumerate(word) if char == k] 
                    for pos in positions:
                        if pos == 1:
                            pos1[k] = pos1[k] + 1;
                        elif pos == 2:
                            pos2[k] = pos2[k] + 1;
                        elif pos == 3:
                            pos3[k] = pos3[k] + 1;
                        elif pos == 4:
                            pos4[k] = pos4[k] + 1;
                        elif pos == 5:
                            pos5[k] = pos5[k] + 1;
                        else:
                            raise ValueError('Only words with 5 letters')                    
            frequencies[k] = freq / (len(self.word_set) * 5)
	        # define emp probability with m-estimate of frequency of that letter
            emp_probabilities[k] = (count + (frequencies[k] * (len(self.word_set) * self.bbq))) / ((len(self.word_set) * self.bbq) + len(self.word_set))
        
        for k in pos1.keys():
            pos1[k] = pos1[k]/len(self.word_set);
            pos2[k] = pos2[k]/len(self.word_set);
            pos3[k] = pos3[k]/len(self.word_set);
            pos4[k] = pos4[k]/len(self.word_set);
            pos5[k] = pos5[k]/len(self.word_set);
            
                            
    def choose_most_probable_word(self):
        if len(self.word_set) == 0:
            return "There is no word that meets the requirements"
        else:
            self.set_all_probabilities()
            max_diversity = 0
            max_diversity_word_list = []
            for word in self.word_set:
                word_letters = "".join(set(word))
                diversity = 0
                for letter in word_letters:
                    if letter not in self.proved_letters:
                        diversity = diversity + 1

                if diversity > max_diversity:
                    max_diversity = diversity
                    max_diversity_word_list = [word]
                elif diversity == max_diversity:
                    max_diversity_word_list.append(word)

            best_word = ""
            best_score = float('-inf')

            for word in max_diversity_word_list:
                word_score = 0
                i = 1
                for letter in word:
                    if letter not in self.proved_letters:
                        emp_probability = emp_probabilities.get(letter)
                        prob_pos = 0
                        if i == 1:
                            prob_pos = pos1[letter];
                        elif i == 2:
                            prob_pos = pos2[letter];
                        elif i == 3:
                            prob_pos = pos3[letter];
                        elif i == 4:
                            prob_pos = pos4[letter];
                        elif i == 5:
                            prob_pos = pos5[letter];
                        else:
                            raise ValueError('Only words with 5 letters')   
                        word_score = word_score + log(emp_probability) + log(prob_pos * self.ketchup)
                    i = i + 1
                if word_score > best_score:
                    best_score = word_score
                    best_word = word

            self.most_probable_word = best_word
            return best_word

    def remove_word_that_not_contains(self, letter):
        temp_set = set()
        # Remove the words that doesn't contains "letter" from the list "result_list"
        for word in self.word_set:
            if letter not in word:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def set_sauce(self, bbq, ketchup):
        self.bbq = bbq
        self.ketcup = ketchup

    def current_most_probable_word(self):
        return self.most_probable_word

    def remove_word_that_contains(self, letter):
        temp_set = set()
        # Remove the words that contains "letter" from the list "result_list"
        for word in self.word_set:
            if letter in word:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def remove_word_that_hasnt_letter_in_pos(self, letter, pos):
        temp_set = set()
        # Remove the words that doesn't have letter in pos from the list "result_list"
        for word in self.word_set:
            if letter not in word[int(pos)]:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def remove_word_that_has_letter_in_pos(self, letter, pos):
        temp_set = set()
        # Remove the words that has letter in pos from the list "result_list"
        for word in self.word_set:
            if letter in word[int(pos)]:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def solve(self, letters: list, colors: list):
        for letter in letters:
            if letter not in self.proved_letters:
                self.proved_letters.add(letter)

            if colors[letters.index(letter)] == "Green":
                self.remove_word_that_not_contains(letter)
                self.remove_word_that_hasnt_letter_in_pos(letter, pos=letters.index(letter))
                if letter not in self.good_letters:
                    self.good_letters.add(letter)
            elif colors[letters.index(letter)] == "Grey":
                if letter not in self.good_letters:
                    self.remove_word_that_contains(letter)
            else:
                self.remove_word_that_not_contains(letter)
                self.remove_word_that_has_letter_in_pos(letter, pos=letters.index(letter))
                if letter not in self.good_letters:
                    self.good_letters.add(letter)
        self.cardinality = abs(self.cardinality - len(self.word_set))

        if len(self.word_set) == 1:
            self.end = True

        return self.choose_most_probable_word()
