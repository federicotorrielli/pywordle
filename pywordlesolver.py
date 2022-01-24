most_probable_letters_in_dataset = ["e", "a", "r", "i", "o", "t", "n", "s"]


class WordleSolver:
    def __init__(self):
        self.word_set = set()
        self.good_letters = set()  # Letters that are in the word and should not be removed
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

    def choose_most_probable_word(self):
        if len(self.word_set) == 0:
            return "There is no word that meets the requirements"
        else:
            max_diversity = 0
            max_diversity_word_list = []
            for word in self.word_set:
                word_letters = "".join(set(word))
                diversity = len(word_letters)
                if diversity > max_diversity:
                    max_diversity = diversity
                    max_diversity_word_list = [word]
                elif diversity == max_diversity:
                    max_diversity_word_list.append(word)

            number_of_frequent_letters = 0
            best_word = ""
            for word in max_diversity_word_list:
                count = 0
                for letter in word:
                    if letter in most_probable_letters_in_dataset:
                        count += 1
                if count > number_of_frequent_letters:
                    number_of_frequent_letters = count
                    best_word = word

            if len(best_word) == 0:
                best_word = max_diversity_word_list[0]

            self.most_probable_word = best_word

    def remove_word_that_not_contains(self, letter):
        temp_set = set()
        # Remove the words that doesn't contains "letter" from the list "result_list"
        for word in self.word_set:
            if letter not in word:
                temp_set.add(word)
        self.word_set = self.word_set - temp_set

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
            if colors[letters.index(letter)] == "Green":
                self.good_letters.add(letter)
                self.remove_word_that_not_contains(letter)
                self.remove_word_that_hasnt_letter_in_pos(letter, pos=letters.index(letter))
            elif colors[letters.index(letter)] == "Grey":
                if letter not in self.good_letters:
                    self.remove_word_that_contains(letter)
            else:
                self.remove_word_that_not_contains(letter)
                self.remove_word_that_has_letter_in_pos(letter, pos=letters.index(letter))
        self.cardinality = abs(self.cardinality - len(self.word_set))
        self.choose_most_probable_word()

        if len(self.word_set) == 1:
            self.end = True
