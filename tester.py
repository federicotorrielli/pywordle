import random

import matplotlib.pyplot as plt
import numpy as np

import pywordlesolver
import progressbar
import concurrent.futures
from words import possible_words


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
        return random.sample(possible_words, self.k)

    def test(self, mayonket):
        """
        Run all the k tests. Return the number of wins and fails
        """
        wins = 0
        tries = []
        sauce1, sauce2 = mayonket[0], mayonket[1]
        for i, solver in enumerate(self.solvers):
            word_to_guess = self.random_words[i]
            colors = ["Grey", "Grey", "Grey", "Grey", "Grey"]
            for j in range(1, 7):  # vogliamo contare il primo tentativo con 1 e l'ultimo con 6
                solver.set_sauce(ketchup=sauce2, mayonnaise=sauce1)
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
    mayonnaise_array = []
    ketchup_array = []
    means_array = []
    means_distribution = []
    for mayonnaise in progressbar.progressbar(range(1, 26)):
        mayonnaise = mayonnaise * 0.12
        count = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            ketchups = [ketchup * 0.12 for ketchup in range(1, 26)]
            futures = [executor.submit(PyWordleTester(1000).test, [mayonnaise, ketchup]) for ketchup in ketchups]
        for future in concurrent.futures.as_completed(futures):
            acc, mean = future.result()
            means_distribution.append([mayonnaise, ketchups[count], mean])
            if acc == max_acc:
                mayonnaise_array.append(mayonnaise)
                ketchup_array.append(ketchups[count])
                means_array.append(mean)
            if acc > max_acc:
                max_acc = acc
                mayonnaise_array = [mayonnaise]
                ketchup_array = [ketchups[count]]
                means_array = [mean]
            count += 1

    print(f"Max accuracy found: {max_acc}")
    x, y, z = [], [], []
    for j in range(0, len(means_distribution)):
        x.append(means_distribution[j][0])
        y.append(means_distribution[j][1])
        z.append(means_distribution[j][2])
    xs = np.array(x)
    ys = np.array(y)
    zs = np.array(z)
    fig = plt.figure(figsize=(24, 15))
    ax = fig.add_subplot(111)
    scat = ax.scatter(xs, ys, c=zs, marker="o", cmap="viridis")
    plt.colorbar(scat)

    ax.set_xlabel('Mayonnaise')
    ax.set_ylabel('Ketchup')
    plt.savefig('means.png')
    for i, elem in enumerate(mayonnaise_array):
        print(f"With mayonnaise = {mayonnaise_array[i]} and ketchup = {ketchup_array[i]} we have mean {means_array[i]}")
