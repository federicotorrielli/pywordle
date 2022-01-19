from pprint import pprint
from random import random

result_list = set()
most_probable_letters_in_5wordenglish = ['e','a','r','i','o','t','n','s']

def prepare_word_set():
    # put the words in "5words.txt" into the set "word_set"
    with open("5words.txt", "r") as f:
        for line in f:
            result_list.add(line.strip().lower())

def choose_starting_word():
    global result_list
    # return a random word from the list "starting_list"
    starting_list = ["frame","graze","windy","paint","gourd","swing","vapes","audio","farts","adieu","ouija","ready","pears","chief","touch","arise","roast","tears","meats","pizza"]
    return starting_list[int(len(starting_list) * random())]

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
            diversity = 0
            for letter in word:
                if letter not in max_diversity_word_list:
                    diversity += 1
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
            
        return best_word

def remove_word_that_doesnt_start_with(letter):
    global result_list
    temp_set = set()
    # Remove the words that doesn't start with "letter" from the list "result_list"
    for word in result_list:
        if not word.startswith(letter):
            temp_set.add(word)
    result_list = result_list - temp_set


def remove_word_that_doesnt_ends_with(letter):
    global result_list
    temp_set = set()
    # Remove the words that doesn't end with "letter" from the list "result_list"
    for word in result_list:
        if not word.endswith(letter):
            temp_set.add(word)
    result_list = result_list - temp_set


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


def main():
    global result_list
    print(f"Most probable starting word: {choose_starting_word()}")
    while True:
        # Ask with the user what he/she wants to do
        print(
            """
        1. Remove words that does not start with a letter
        2. Remove words that does not end with a letter
        3. Remove words that contains a letter
        4. Remove words that does not contain a letter
        5. Remove words that has NOT a letter in a certain position
        6. Gimme another word!
        7. Exit
        """
        )
        choice = input("Enter your choice: ")
        if choice == "7":
            break
        elif choice == "1":
            letter = input("Enter the letter: ")
            remove_word_that_doesnt_start_with(letter)
        elif choice == "2":
            letter = input("Enter the letter: ")
            remove_word_that_doesnt_ends_with(letter)
        elif choice == "3":
            letter = input("Enter the letter: ")
            remove_word_that_contains(letter)
        elif choice == "4":
            letter = input("Enter the letter: ")
            remove_word_that_not_contains(letter)
        elif choice == "5":
            letter = input("Enter the letter: ")
            pos = input("Enter the position: ")
            remove_word_that_hasnt_letter_in_pos(letter, pos)
        elif choice == "6":
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
