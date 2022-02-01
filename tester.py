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

    def test(self, secret_sauce=0.05):
        """
        Run all the k tests. Return the number of wins and fails
        """
        wins = 0
        for i, solver in enumerate(self.solvers):
            word_to_guess = self.random_words[i]
            colors = ["Grey", "Grey", "Grey", "Grey", "Grey"]
            for j in range(6):  # 6 possible guesses
                current_guess = [letter for letter in solver.current_most_probable_word()]
                colors = self.get_colors(current_guess, colors, word_to_guess)
                if solver.solve(current_guess, colors, secret_sauce) == word_to_guess:
                    wins += 1
                    break
        return wins, self.k - wins

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
    max_wins = 0
    max_wins_array = []
    for parameter in range(1, 100):
        parameter = parameter/1000
        tester = PyWordleTester(100)
        wins, fails = tester.test(parameter)
        if wins == max_wins:
            max_wins_array.append(parameter)
        if wins > max_wins:
            max_wins = wins
            max_wins_array = [parameter]
            print(f"Next Max wins found: {max_wins} with parameter {parameter} | {max_wins_array}")
    print(f"Max wins found: {max_wins} with parameter {max_wins_array}")
