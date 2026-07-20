/*
 * Copyright 2022-2026 Federico Torrielli and Lorenzo Sciandra
 * Licensed under the EUPL v. 1.2 only.
 */

#include "solver.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

static void assert_feedback(const char *answer, const char *guess,
                            const Tile expected[WORD_LENGTH])
{
    Tile actual[WORD_LENGTH];
    size_t position;

    wordle_feedback(answer, guess, actual);
    for (position = 0; position < WORD_LENGTH; position++) {
        assert(actual[position] == expected[position]);
    }
}

static void assert_solved(const char *answer)
{
    Solver *solver = solver_create();
    size_t attempt;

    assert(solver != NULL);
    for (attempt = 0; attempt < 20; attempt++) {
        const char *guess = solver_suggestion(solver);
        Tile feedback[WORD_LENGTH];

        assert(guess != NULL);
        if (strcmp(guess, answer) == 0) {
            solver_destroy(solver);
            return;
        }
        wordle_feedback(answer, guess, feedback);
        assert(solver_apply_feedback(solver, guess, feedback));
        assert(solver_remaining(solver) > 0);
    }
    assert(!"solver did not reach the answer within 20 guesses");
}

int main(void)
{
    const Tile simple[WORD_LENGTH] = {
        TILE_GREEN, TILE_GREY, TILE_GREY, TILE_GREEN, TILE_GREEN
    };
    const Tile repeated[WORD_LENGTH] = {
        TILE_YELLOW, TILE_GREEN, TILE_GREY, TILE_YELLOW, TILE_GREY
    };
    Solver *solver;
    size_t initial_count;

    assert_feedback("amble", "apple", simple);
    assert_feedback("eerie", "refer", repeated);

    solver = solver_create();
    assert(solver != NULL);
    initial_count = solver_remaining(solver);
    assert(initial_count > 0);
    assert(solver_suggestion(solver) != NULL);
    assert(solver_apply_feedback(solver, "refer", repeated));
    assert(solver_remaining(solver) > 0);
    assert(solver_remaining(solver) < initial_count);
    assert(solver_suggestion(solver) != NULL);
    solver_destroy(solver);

    assert_solved("eerie");
    assert_solved("sissy");
    assert_solved("allee");

    puts("solver tests passed");
    return 0;
}
