import toga
import pywordlesolver
from toga.style.pack import COLUMN, CENTER, ROW, Pack

letters = {}
colors = {}
ready = False
start = True # True if the game has not started yet
solver = pywordlesolver.WordleSolver()


def change_letters(widget):
    global ready
    letters[widget.id] = widget.value.lower()
    if len(letters) == 5:
        ready = True
    else:
        ready = False


def change_color(widget):
    """
    This function will change the color of the button that has been pressed.
    """
    if widget.label == 'Grey':
        widget.label = 'Yellow'
        widget.style.update(background_color='yellow')
    elif widget.label == 'Yellow':
        widget.label = 'Green'
        widget.style.update(background_color='green')
    elif widget.label == 'Green':
        widget.label = 'Grey'
        widget.style.update(background_color='grey')
    colors[widget.id] = widget.label


def start_solver(output_text, first_row_pack):
    """
    This function will start the solver and output the most probable word.
    """
    global solver, start
    start = False
    if ready:
        solver.solve(list(letters.values()), list(colors.values()))
        output_text.text = solver.most_probable_word.upper()
        for count, letters_holder in enumerate(first_row_pack):
            letters_holder.value = solver.most_probable_word[count]
    else:
        output_text.text = 'Please fill all the inputs'


def build(app):
    """
    The app should be divided in 3 rows: the first will contain 5 inputs, one for
    each letter that we will use in the Wordle. The second row will contain 5 selectors
    for colors, each under the letter in the previous row. The second row's possible colors
    are the same as Wordle colors: grey, yellow or green. On the same row it will be a button
    to output the most probable word to the following (3rd) row.
    """
    global start, solver
    program_box = toga.Box()
    first_row = toga.Box()  # Row for the letters
    second_row = toga.Box()  # Row for the colors
    third_row = toga.Box()  # Row for the output
    last_row = toga.Box()  # Row for the button to start the solver
    # We now define all the 5 inputs for the first row
    first_row_pack = [toga.TextInput(style=Pack(flex=1, padding_left=10), on_change=change_letters) for _ in range(5)]
    for el in first_row_pack:
        el.style.update(width=50, text_align=CENTER)
        first_row.add(el)
    # We now define all the 5 buttons for the second row: when pressed, they should change color
    second_row_pack = [toga.Button('Grey', style=Pack(flex=1, padding_left=10, width=50), on_press=change_color) for _
                       in range(5)]
    for el in second_row_pack:
        colors[el.id] = el.label
        second_row.add(el)
    # We now define the output text
    output_text = toga.Label(solver.most_probable_word.upper(), style=Pack(flex=1, text_align=CENTER, padding_left=10, width=300, font_weight='bold', color='green'))
    third_row.add(output_text)
    # We now define the button to start the solver
    start_button = toga.Button('Start', style=Pack(flex=1, padding_left=10, width=300),
                               on_press=lambda widget: start_solver(output_text, first_row_pack))
    last_row.add(start_button)

    first_row.style.update(direction=ROW, padding_top=30, padding_bottom=10, padding_left=150)
    second_row.style.update(direction=ROW, padding_top=30, padding_bottom=10, padding_left=150)
    third_row.style.update(direction=ROW, padding_top=30, padding_bottom=10, padding_left=150)
    last_row.style.update(direction=ROW, padding_top=30, padding_bottom=10, padding_left=150)
    program_box.add(first_row)
    program_box.add(second_row)
    program_box.add(third_row)
    program_box.add(last_row)
    program_box.style.update(direction=COLUMN)
    return program_box


def main():
    return toga.App('Wordle Solver', 'org.pywordlesolver', startup=build)


if __name__ == '__main__':
    app = main()
    app.main_loop()
