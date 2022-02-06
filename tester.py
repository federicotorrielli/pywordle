import pywordlesolver
import random


class PyWordleTester:
    """
    This class is used to test PyWordle functions.
    k: number of passes (tests) on pywordlesolver
    solvers: list of solvers to test
    """

    def __init__(self, k):
        self.k = k
        self.solvers = [pywordlesolver.WordleSolver() for _ in range(k)]
        self.random_words = self.prepare_random_words()

    def prepare_random_words(self):
        """
        Take from 5words.txt k random words and return a list of them
        """
        with open('5words.txt', 'r') as f:
            words = f.read().splitlines()
        return random.sample(words, self.k)

    def test(self, bbq, ketchup):
        """
        Run all the k tests. Return the number of wins and fails
        """
        wins = 0
        tries = []
        for i, solver in enumerate(self.solvers):
            word_to_guess = self.random_words[i]
            colors = ["Grey", "Grey", "Grey", "Grey", "Grey"]
            for j in range(1, 7):  # vogliamo contare il primo tentativo con 1 e l'ultimo con 6
                solver.set_sauce(bbq,ketchup)
                if j == 1:
                    current_guess = [letter for letter in solver.choose_most_probable_word()]
                else:
                    current_guess = [letter for letter in solver.current_most_probable_word()]
                colors = self.get_colors(current_guess, colors, word_to_guess)
                if solver.solve(current_guess, colors) == word_to_guess:
                    wins += 1
                    tries.append(j)
                    break
        acc = wins / self.k
        mean = sum(tries) / len(tries)
        return acc, mean

    def get_colors(self, current_guess, current_colors, word_to_guess):
        """
        Given the current 5 letter word, generate a list of colors like Wordle does
        """
        for index, letter in enumerate(current_guess):
            # If the letter in current_guess is exactly in the same spot in word_to_guess
            # Then the color in current_colors corresponding to the index of the letter will be green
            if letter == word_to_guess[index]:
                current_colors[index] = "Green"
            # If the letter in current_guess is in word_to_guess but not in the same exact spot
            # Then the color in current_colors corresponding to the index of the letter will be yellow
            elif letter in word_to_guess:
                current_colors[index] = "Yellow"
            # If the letter in current_guess is not in word_to_guess
            # Then the color in current_colors corresponding to the index of the letter will be grey
            else:
                current_colors[index] = "Grey"
        return current_colors


if __name__ == "__main__":
    max_acc = 0
    bbq_array = []
    ketchup_array = []
    means_array = []
    for bbq in range(1, 61):
        bbq = bbq * 0.05
        for ketchup in range(1, 41):
            ketchup = ketchup * 0.05
            tester = PyWordleTester(1000)
            acc, mean = tester.test(bbq, ketchup)
            if acc == max_acc:
                bbq_array.append(bbq)
                ketchup_array.append(ketchup)
                means_array.append(mean)
            if acc > max_acc:
                max_acc = acc
                bbq_array = [bbq]
                ketchup_array = [ketchup]
                means_array = [mean]

    print(f"Max accuracy found: {max_acc}")
    for i, elem in enumerate(bbq_array):
        print(f"With bbq = {bbq_array[i]} and ketchup = {ketchup_array[i]} we have mean {means_array[i]}")
