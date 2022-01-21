from pprint import pprint
from random import random

result_list = set()
most_probable_letters_in_5wordenglish = ["e", "a", "r", "i", "o", "t", "n", "s"]


def prepare_word_set():
    # put the words in "5words.txt" into the set "word_set"
    with open("5words.txt", "r") as f:
        for line in f:
            result_list.add(line.strip().lower())

def choose_most_probable_word():
    global result_list
    # The most probable word in the list is defined as the word that has the most diverse letters in it
    # We want to count the number of diverse letters in each word and return the word with the most diverse letters
    if len(result_list) == 0:
        print("There is no word that meets the requirements")
        return ""
    else:
        max_diversity = 0
        max_diversity_word_list = []
        for word in result_list:
            word_letters = "".join(set(word))
            diversity = len(word_letters)
            if diversity > max_diversity:
                max_diversity = diversity
                max_diversity_word_list = []
                max_diversity_word_list.append(word)
            elif diversity == max_diversity:
                max_diversity_word_list.append(word)

        number_of_frequent_letters = 0
        best_word = ""
        for word in max_diversity_word_list:
            count = 0
            for letter in word:
                if letter in most_probable_letters_in_5wordenglish:
                    count += 1
            if count > number_of_frequent_letters:
                number_of_frequent_letters = count
                best_word = word
        
        if len(best_word) == 0:
            best_word =  max_diversity_word_list[0]
        
        return best_word


def remove_word_that_not_contains(letter):
    global result_list
    temp_set = set()
    # Remove the words that doesn't contains "letter" from the list "result_list"
    for word in result_list:
        if letter not in word:
            temp_set.add(word)
    result_list = result_list - temp_set


def remove_word_that_contains(letter):
    global result_list
    temp_set = set()
    # Remove the words that contains "letter" from the list "result_list"
    for word in result_list:
        if letter in word:
            temp_set.add(word)
    result_list = result_list - temp_set


def remove_word_that_hasnt_letter_in_pos(letter, pos):
    global result_list
    temp_set = set()
    # Remove the words that doesn't have letter in pos from the list "result_list"
    for word in result_list:
        if letter not in word[int(pos) - 1]:
            temp_set.add(word)
    result_list = result_list - temp_set


def remove_word_that_has_letter_in_pos(letter, pos):
    global result_list
    temp_set = set()
    # Remove the words that has letter in pos from the list "result_list"
    for word in result_list:
        if letter in word[int(pos) - 1]:
            temp_set.add(word)
    result_list = result_list - temp_set


def process_input(input_string, letter=True, position=False):
    """
    Process the input string and verify that if letter==True then it must be a character, not a number
    while if it is a position, it must be a number, not a character. In neither cases, it must not be
    a special character.
    """
    if not input_string.isalnum():
        raise ValueError("The input must be a character or a number")
    if letter:
        if not input_string.isalpha():
            raise ValueError("The input must be a character")
    elif position:
        if not input_string.isdigit():
            raise ValueError("The input must be a number")
    return input_string


def main():
    global result_list
    print(f"Most probable starting word: {choose_most_probable_word()}")
    while True:
        print(
        """
        1. Remove words that contains a letter
        2. Remove words that does NOT contain a letter
        3. Remove words that has NOT a letter in a certain position
        4. Remove words that has a letter in a certain position
        5. Gimme another word!
        6. Exit
        """
        )
        choice = input("Enter your choice: ")
        if choice == "6":
            break
        elif choice == "1":
            letter = process_input(input("Enter the letter: "))
            remove_word_that_contains(letter)
        elif choice == "2":
            letter = process_input(input("Enter the letter: "))
            remove_word_that_not_contains(letter)
        elif choice == "3":
            letter = process_input(input("Enter the letter: "))
            pos = process_input(
                input("Enter the position: "), letter=False, position=True
            )
            remove_word_that_hasnt_letter_in_pos(letter, pos)
        elif choice == "4":
            letter = process_input(input("Enter the letter: "))
            pos = process_input(
                input("Enter the position: "), letter=False, position=True
            )
            remove_word_that_has_letter_in_pos(letter, pos)
        elif choice == "5":
            result_list.remove(word)
            word = choose_most_probable_word()
            print(f"Most probable word: {word}")
            continue
        else:
            print("Invalid choice")
        word = choose_most_probable_word()
        print(f"Most probable word: {word}")


if __name__ == "__main__":
    prepare_word_set()
    main()
