/*
 * Copyright 2022-2026 Federico Torrielli and Lorenzo Sciandra
 * Licensed under the EUPL v. 1.2 only.
 */

#include <ncurses.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "solver.h"

#define MAX_ATTEMPTS 6
#define ESCAPE_KEY 27

static bool row_complete(const char row[WORD_LENGTH + 1])
{
    size_t position;

    for (position = 0; position < WORD_LENGTH; position++) {
        if (row[position] == '\0') {
            return false;
        }
    }
    return true;
}

static bool solved(const Tile feedback[WORD_LENGTH])
{
    size_t position;

    for (position = 0; position < WORD_LENGTH; position++) {
        if (feedback[position] != TILE_GREEN) {
            return false;
        }
    }
    return true;
}

static int tile_attribute(Tile tile, bool colour_enabled)
{
    if (!colour_enabled) {
        return tile == TILE_GREY ? A_NORMAL : A_BOLD;
    }
    if (tile == TILE_GREEN) {
        return COLOR_PAIR(COLOR_GREEN_PAIR);
    }
    if (tile == TILE_YELLOW) {
        return COLOR_PAIR(COLOR_YELLOW_PAIR);
    }
    return COLOR_PAIR(COLOR_GREY_PAIR);
}

static void draw_ui(WINDOW *window,
                    char guesses[MAX_ATTEMPTS][WORD_LENGTH + 1],
                    Tile feedback[MAX_ATTEMPTS][WORD_LENGTH],
                    size_t current_row, size_t current_column,
                    const char *suggestion, size_t remaining,
                    bool colour_enabled, const char *status)
{
    size_t row;

    werase(window);
    box(window, 0, 0);
    mvwprintw(window, 1, 2, "wordle-solver");
    mvwprintw(window, 3, 2,
              "Left/Right: move  Space: colour  Enter: submit  Esc: quit");
    mvwprintw(window, 5, 2, "Guesses:");

    for (row = 0; row < MAX_ATTEMPTS; row++) {
        size_t column;

        mvwprintw(window, 7 + (int)row * 2, 4, "%zu: ", row + 1);
        for (column = 0; column < WORD_LENGTH; column++) {
            char letter = guesses[row][column];
            int attribute = tile_attribute(feedback[row][column],
                                           colour_enabled);

            if (letter >= 'a' && letter <= 'z') {
                letter = (char)(letter - 'a' + 'A');
            } else {
                letter = '_';
            }
            wattron(window, attribute);
            if (row == current_row && column == current_column) {
                wattron(window, A_REVERSE);
            }
            mvwprintw(window, 7 + (int)row * 2,
                      10 + (int)column * 3, " %c ", letter);
            wattroff(window, A_REVERSE);
            wattroff(window, attribute);
        }
    }

    mvwprintw(window, 20, 2, "Suggestion: %-5s",
              suggestion == NULL ? "-----" : suggestion);
    mvwprintw(window, 21, 2, "Remaining: %zu", remaining);
    if (status != NULL) {
        mvwprintw(window, 22, 2, "%s", status);
    } else if (remaining == 1) {
        mvwprintw(window, 22, 2, "One candidate remains.");
    } else if (remaining == 0) {
        mvwprintw(window, 22, 2, "No candidate matches that feedback.");
    }
    wrefresh(window);
}

static bool initialise_colours(void)
{
    if (!has_colors() || start_color() == ERR) {
        return false;
    }
    init_pair(COLOR_GREY_PAIR, COLOR_WHITE, COLOR_BLACK);
    init_pair(COLOR_YELLOW_PAIR, COLOR_BLACK, COLOR_YELLOW);
    init_pair(COLOR_GREEN_PAIR, COLOR_BLACK, COLOR_GREEN);
    return true;
}

int main(void)
{
    Solver *solver = solver_create();
    char guesses[MAX_ATTEMPTS][WORD_LENGTH + 1] = {{0}};
    Tile feedback[MAX_ATTEMPTS][WORD_LENGTH] = {{TILE_GREY}};
    size_t current_row = 0;
    size_t current_column = 0;
    bool finished = false;
    bool running = true;
    bool colour_enabled;
    const char *status = NULL;
    const char *suggestion;
    WINDOW *window;

    if (solver == NULL) {
        fputs("wordle-solver: could not allocate solver state\n", stderr);
        return EXIT_FAILURE;
    }
    if (initscr() == NULL) {
        solver_destroy(solver);
        fputs("wordle-solver: could not initialise the terminal\n", stderr);
        return EXIT_FAILURE;
    }
    if (LINES < UI_HEIGHT || COLS < UI_WIDTH) {
        endwin();
        solver_destroy(solver);
        fprintf(stderr, "wordle-solver: terminal must be at least %dx%d\n",
                UI_WIDTH, UI_HEIGHT);
        return EXIT_FAILURE;
    }

    cbreak();
    noecho();
    curs_set(0);
    colour_enabled = initialise_colours();
    window = newwin(UI_HEIGHT, UI_WIDTH, 0, 0);
    if (window == NULL) {
        endwin();
        solver_destroy(solver);
        fputs("wordle-solver: could not create the terminal window\n", stderr);
        return EXIT_FAILURE;
    }
    keypad(window, true);
    suggestion = solver_suggestion(solver);

    while (running) {
        int key;

        draw_ui(window, guesses, feedback, current_row, current_column,
                suggestion, solver_remaining(solver), colour_enabled, status);
        key = wgetch(window);
        status = NULL;

        switch (key) {
        case ESCAPE_KEY:
            running = false;
            break;
        case KEY_LEFT:
            if (current_column > 0) {
                current_column--;
            }
            break;
        case KEY_RIGHT:
            if (current_column + 1 < WORD_LENGTH) {
                current_column++;
            }
            break;
        case ' ':
            if (!finished) {
                feedback[current_row][current_column] =
                    (Tile)((feedback[current_row][current_column] + 1) % 3);
            }
            break;
        case '\n':
        case KEY_ENTER:
            if (finished) {
                break;
            }
            if (!row_complete(guesses[current_row])) {
                status = "Enter all five letters before submitting.";
                break;
            }
            solver_apply_feedback(solver, guesses[current_row],
                                  feedback[current_row]);
            suggestion = solver_suggestion(solver);
            if (solved(feedback[current_row])) {
                status = "Solved.";
                finished = true;
            } else if (solver_remaining(solver) == 0) {
                finished = true;
            } else if (current_row + 1 == MAX_ATTEMPTS) {
                status = "No attempts remain.";
                finished = true;
            } else {
                current_row++;
                current_column = 0;
            }
            break;
        case KEY_BACKSPACE:
        case 127:
        case '\b':
            if (!finished) {
                if (guesses[current_row][current_column] != '\0') {
                    guesses[current_row][current_column] = '\0';
                } else if (current_column > 0) {
                    current_column--;
                    guesses[current_row][current_column] = '\0';
                }
            }
            break;
        default:
            if (!finished && key >= 'A' && key <= 'Z') {
                key = key - 'A' + 'a';
            }
            if (!finished && key >= 'a' && key <= 'z') {
                guesses[current_row][current_column] = (char)key;
                if (current_column + 1 < WORD_LENGTH) {
                    current_column++;
                }
            }
            break;
        }
    }

    delwin(window);
    endwin();
    solver_destroy(solver);
    return EXIT_SUCCESS;
}
