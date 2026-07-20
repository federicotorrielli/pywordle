/*
 * Copyright 2022-2026 Federico Torrielli and Lorenzo Sciandra
 * Licensed under the EUPL v. 1.2 only.
 */

#include "solver.h"

#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "words.h"

#define ALPHABET_SIZE 26

struct Solver {
    bool active[WORD_COUNT];
    bool guessed[ALPHABET_SIZE];
    bool fixed[WORD_LENGTH];
    size_t remaining;
};

static int letter_index(char letter)
{
    return letter - 'a';
}

static bool valid_word(const char *word)
{
    size_t position;

    if (word == NULL || strlen(word) != WORD_LENGTH) {
        return false;
    }

    for (position = 0; position < WORD_LENGTH; position++) {
        if (word[position] < 'a' || word[position] > 'z') {
            return false;
        }
    }
    return true;
}

Solver *solver_create(void)
{
    Solver *solver = malloc(sizeof(*solver));

    if (solver == NULL) {
        return NULL;
    }

    memset(solver->active, 1, sizeof(solver->active));
    memset(solver->guessed, 0, sizeof(solver->guessed));
    memset(solver->fixed, 0, sizeof(solver->fixed));
    solver->remaining = WORD_COUNT;
    return solver;
}

void solver_destroy(Solver *solver)
{
    free(solver);
}

size_t solver_remaining(const Solver *solver)
{
    return solver == NULL ? 0 : solver->remaining;
}

void wordle_feedback(const char *answer, const char *guess,
                     Tile feedback[WORD_LENGTH])
{
    bool claimed[WORD_LENGTH] = {false};
    size_t guess_position;
    size_t answer_position;

    for (guess_position = 0; guess_position < WORD_LENGTH; guess_position++) {
        feedback[guess_position] = TILE_GREY;
        if (guess[guess_position] == answer[guess_position]) {
            feedback[guess_position] = TILE_GREEN;
            claimed[guess_position] = true;
        }
    }

    for (guess_position = 0; guess_position < WORD_LENGTH; guess_position++) {
        if (feedback[guess_position] == TILE_GREEN) {
            continue;
        }
        for (answer_position = 0; answer_position < WORD_LENGTH;
             answer_position++) {
            if (!claimed[answer_position] &&
                guess[guess_position] == answer[answer_position]) {
                feedback[guess_position] = TILE_YELLOW;
                claimed[answer_position] = true;
                break;
            }
        }
    }
}

static bool same_feedback(const Tile left[WORD_LENGTH],
                          const Tile right[WORD_LENGTH])
{
    return memcmp(left, right, sizeof(Tile) * WORD_LENGTH) == 0;
}

bool solver_apply_feedback(Solver *solver, const char *guess,
                           const Tile feedback[WORD_LENGTH])
{
    size_t word_index;
    size_t position;

    if (solver == NULL || feedback == NULL || !valid_word(guess)) {
        return false;
    }

    for (position = 0; position < WORD_LENGTH; position++) {
        if (feedback[position] < TILE_GREY ||
            feedback[position] > TILE_GREEN) {
            return false;
        }
    }

    for (position = 0; position < WORD_LENGTH; position++) {
        solver->guessed[letter_index(guess[position])] = true;
        if (feedback[position] == TILE_GREEN) {
            solver->fixed[position] = true;
        }
    }

    for (word_index = 0; word_index < WORD_COUNT; word_index++) {
        Tile candidate_feedback[WORD_LENGTH];

        if (!solver->active[word_index]) {
            continue;
        }
        wordle_feedback(WORDS[word_index], guess, candidate_feedback);
        if (!same_feedback(candidate_feedback, feedback)) {
            solver->active[word_index] = false;
            solver->remaining--;
        }
    }
    return true;
}

static void count_letters(const Solver *solver,
                          size_t present[ALPHABET_SIZE],
                          size_t positional[WORD_LENGTH][ALPHABET_SIZE])
{
    size_t word_index;

    memset(present, 0, sizeof(size_t) * ALPHABET_SIZE);
    memset(positional, 0,
           sizeof(size_t) * WORD_LENGTH * ALPHABET_SIZE);

    for (word_index = 0; word_index < WORD_COUNT; word_index++) {
        bool seen[ALPHABET_SIZE] = {false};
        size_t position;

        if (!solver->active[word_index]) {
            continue;
        }
        for (position = 0; position < WORD_LENGTH; position++) {
            int index = letter_index(WORDS[word_index][position]);

            positional[position][index]++;
            if (!seen[index]) {
                present[index]++;
                seen[index] = true;
            }
        }
    }
}

static int word_diversity(const Solver *solver, const char *word)
{
    bool seen[ALPHABET_SIZE] = {false};
    int diversity = 0;
    size_t position;

    for (position = 0; position < WORD_LENGTH; position++) {
        int index = letter_index(word[position]);

        if (!seen[index] && !solver->guessed[index]) {
            diversity++;
            seen[index] = true;
        }
    }
    return diversity;
}

static double word_score(
    const Solver *solver, const char *word,
    const size_t present[ALPHABET_SIZE],
    size_t positional[WORD_LENGTH][ALPHABET_SIZE])
{
    double score = 0.0;
    size_t position;

    for (position = 0; position < WORD_LENGTH; position++) {
        int index;
        double presence_probability;
        double position_probability;

        if (solver->fixed[position]) {
            continue;
        }
        index = letter_index(word[position]);
        presence_probability = (double)present[index] / solver->remaining;
        position_probability =
            (double)positional[position][index] / solver->remaining;
        score += LETTER_WEIGHT * log(presence_probability);
        score += POSITION_WEIGHT * log(position_probability);
    }
    return score;
}

const char *solver_suggestion(Solver *solver)
{
    size_t present[ALPHABET_SIZE];
    size_t positional[WORD_LENGTH][ALPHABET_SIZE];
    const char *best_word = NULL;
    double best_score = -INFINITY;
    int best_diversity = -1;
    size_t word_index;

    if (solver == NULL || solver->remaining == 0) {
        return NULL;
    }

    count_letters(solver, present, positional);
    for (word_index = 0; word_index < WORD_COUNT; word_index++) {
        int diversity;
        double score;

        if (!solver->active[word_index]) {
            continue;
        }
        diversity = word_diversity(solver, WORDS[word_index]);
        if (diversity < best_diversity) {
            continue;
        }
        score = word_score(solver, WORDS[word_index], present, positional);
        if (diversity > best_diversity || score > best_score) {
            best_word = WORDS[word_index];
            best_diversity = diversity;
            best_score = score;
        }
    }
    return best_word;
}
