/*
 * Copyright 2022-2026 Federico Torrielli and Lorenzo Sciandra
 * Licensed under the EUPL v. 1.2 only.
 */

#ifndef SOLVER_H
#define SOLVER_H

#include <stdbool.h>
#include <stddef.h>

#define WORD_LENGTH 5

typedef enum {
    TILE_GREY,
    TILE_YELLOW,
    TILE_GREEN
} Tile;

typedef struct Solver Solver;

Solver *solver_create(void);
void solver_destroy(Solver *solver);
size_t solver_remaining(const Solver *solver);
const char *solver_suggestion(Solver *solver);
bool solver_apply_feedback(Solver *solver, const char *guess,
                           const Tile feedback[WORD_LENGTH]);
void wordle_feedback(const char *answer, const char *guess,
                     Tile feedback[WORD_LENGTH]);

#endif /* SOLVER_H */
