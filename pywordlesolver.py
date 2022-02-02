from math import log

frequencies = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0,
               "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}

emp_probabilities = frequencies


class WordleSolver:
    def __init__(self):
        self.word_set = set()
        self.good_letters = set()  # Letters that are in the word and should not be removed
        self.proved_letters = set()  # Letters used in previous guess
        self.most_probable_word = ""
        self.prepare_word_set()
        self.original_cardinality = len(self.word_set)
        self.cardinality = len(self.word_set)
        self.choose_most_probable_word()
        self.end = False

    def prepare_word_set(self):
        with open("5words.txt", "r") as f:
            for line in f:
                self.word_set.add(line.strip().lower())

    def set_dictionary(self):
        for k in frequencies.keys():
            freq = 0
            for word in self.word_set:
                freq = freq + word.count(k)
            frequencies[k] = freq / (len(self.word_set) * 5)

    def set_empprobabilities(self, secret_sauce):
        for k in emp_probabilities.keys():
            count = 0
            for word in self.word_set:
                if k in word:
                    count = count + 1
            # define emp probability with m-estimate of frequency of that letter
            emp_probabilities[k] = (count + (frequencies[k] * (len(self.word_set) * secret_sauce))) / ((len(self.word_set) * secret_sauce) + len(self.word_set))

    def choose_most_probable_word(self, secret_sauce=0.947):
        if len(self.word_set) == 0:
            return "There is no word that meets the requirements"
        else:
            self.set_dictionary()
            self.set_empprobabilities(secret_sauce)
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
                different_letters = "".join(set(word))
                for letter in different_letters:
                    if letter not in self.proved_letters:
                        emp_probability = emp_probabilities.get(letter)
                        word_score = word_score + log(emp_probability)
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

    def solve(self, letters: list, colors: list, secret_sauce=0.947):
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

        return self.choose_most_probable_word(secret_sauce)
