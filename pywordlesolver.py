from pprint import pprint

result_list = set()


def prepare_word_set():
    # put the words in "5words.txt" into the set "word_set"
    with open("5words.txt", "r") as f:
        for line in f:
            result_list.add(line.strip().lower())


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
            print("Most probable word: " + str(result_list.pop()))
            continue
        else:
            print("Invalid choice")
        # We always want to print a random word from the list "result_list"
        print("Most probable word: " + str(result_list.pop()))


if __name__ == "__main__":
    prepare_word_set()
    main()
