from math import log
from words import possible_words


class WordleSolver:
    def __init__(self, bbq=1.5, ketchup=1.6, mayonnaise=1.0):
        self.frequencies = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0,
                            "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0,
                            "w": 0, "x": 0, "y": 0, "z": 0}

        self.emp_probabilities = self.frequencies.copy()
        self.pos1 = self.frequencies.copy()
        self.pos2 = self.frequencies.copy()
        self.pos3 = self.frequencies.copy()
        self.pos4 = self.frequencies.copy()
        self.pos5 = self.frequencies.copy()
        self.word_set = set()
        self.good_letters = set()  # Letters that are in the word and should not be removed
        self.proved_letters = set()  # Letters used in previous guess
        self.green_letters = set()  # Letters fixed
        self.most_probable_word = ""
        self.ketchup = ketchup
        self.bbq = bbq
        self.mayonnaise = mayonnaise
        self.prepare_word_set()
        self.original_cardinality = len(self.word_set)
        self.cardinality = len(self.word_set)
        self.end = False
        self.choose_most_probable_word()

    def prepare_word_set(self):
        self.word_set = set(possible_words)

    def set_all_probabilities(self):
        for k in self.frequencies.keys():
            freq = 0
            count = 0
            for word in self.word_set:
                if k in word:
                    freq = freq + word.count(k)
                    count = count + 1
                    positions = [pos + 1 for pos, char in enumerate(word) if char == k]
                    for pos in positions:
                        if pos == 1:
                            self.pos1[k] = self.pos1[k] + 1
                        elif pos == 2:
                            self.pos2[k] = self.pos2[k] + 1
                        elif pos == 3:
                            self.pos3[k] = self.pos3[k] + 1
                        elif pos == 4:
                            self.pos4[k] = self.pos4[k] + 1
                        elif pos == 5:
                            self.pos5[k] = self.pos5[k] + 1
                        else:
                            raise ValueError('Only words with 5 letters')
            self.frequencies[k] = freq / (len(self.word_set) * 5)
            # define emp probability with m-estimate of frequency of that letter
            self.emp_probabilities[k] = (count + (self.frequencies[k] * (len(self.word_set) * self.bbq))) / (
                    (len(self.word_set) * self.bbq) + len(self.word_set))

        for k in self.pos1.keys():
            self.pos1[k] = self.pos1[k] / len(self.word_set)
            self.pos2[k] = self.pos2[k] / len(self.word_set)
            self.pos3[k] = self.pos3[k] / len(self.word_set)
            self.pos4[k] = self.pos4[k] / len(self.word_set)
            self.pos5[k] = self.pos5[k] / len(self.word_set)

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
                    if letter not in self.green_letters:
                        emp_probability = self.emp_probabilities.get(letter)
                        if i == 1:
                            prob_pos = self.pos1[letter]
                        elif i == 2:
                            prob_pos = self.pos2[letter]
                        elif i == 3:
                            prob_pos = self.pos3[letter]
                        elif i == 4:
                            prob_pos = self.pos4[letter]
                        elif i == 5:
                            prob_pos = self.pos5[letter]
                        else:
                            raise ValueError('Only words with 5 letters')
                        word_score = word_score + log(emp_probability * self.mayonnaise) + log(prob_pos * self.ketchup)
                    i = i + 1
                if word_score > best_score:
                    best_score = word_score
                    best_word = word

            self.most_probable_word = best_word
            return best_word

    def remove_word_that_not_contains(self, letter):
        temp_set = set()
        # Remove the words that doesn't contain "letter" from the list "result_list"
        for word in self.word_set:
            if letter not in word:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def set_sauce(self, bbq=1.5, ketchup=1.6, mayonnaise=1.0):
        """
        Why is it spicy?
        """
        self.bbq = bbq
        self.ketchup = ketchup
        self.mayonnaise = mayonnaise

    def current_most_probable_word(self):
        return self.most_probable_word

    def remove_word_that_contains(self, letter):
        temp_set = set()
        # Remove the words that contain "letter" from the list "result_list"
        for word in self.word_set:
            if letter in word:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

    def remove_word_that_hasnt_letter_in_pos(self, letter, pos):
        temp_set = set()
        # Remove the words that doesn't have a letter in pos from the list "result_list"
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
                self.green_letters.add(letter)
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
