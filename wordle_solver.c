#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <ncurses.h>
#include "config.h"
#include "words.h"

#define WORD_LEN 5
#define MAX_ATTEMPTS 6
#define ALPHA_SIZE 26

typedef enum { GREY = 0, YELLOW = 1, GREEN = 2 } ColorState;

typedef struct {
    char word[WORD_LEN + 1];
    int active;
} WordEntry;

typedef struct {
    WordEntry words[WORD_COUNT];
    int count;
    double freq[ALPHA_SIZE];
    double emp_prob[ALPHA_SIZE];
    double pos_prob[5][ALPHA_SIZE];
    char proved_letters[ALPHA_SIZE];
    char good_letters[ALPHA_SIZE];
    char green_letters[ALPHA_SIZE];
    double bbq, ketchup, mayonnaise;
} Solver;

static inline int char_to_idx(char c) {
    return tolower(c) - 'a';
}

static inline char idx_to_char(int idx) {
    return 'a' + idx;
}

void init_solver(Solver *s) {
    s->bbq = BBQ;
    s->ketchup = KETCHUP;
    s->mayonnaise = MAYONNAISE;
    s->count = WORD_COUNT;
    
    memset(s->proved_letters, 0, ALPHA_SIZE);
    memset(s->good_letters, 0, ALPHA_SIZE);
    memset(s->green_letters, 0, ALPHA_SIZE);
    
    for (int i = 0; i < WORD_COUNT; i++) {
        strcpy(s->words[i].word, possible_words[i]);
        s->words[i].active = 1;
    }
}

void calc_probabilities(Solver *s) {
    int letter_count[ALPHA_SIZE] = {0};
    int letter_freq[ALPHA_SIZE] = {0};
    
    memset(s->freq, 0, sizeof(s->freq));
    memset(s->emp_prob, 0, sizeof(s->emp_prob));
    memset(s->pos_prob, 0, sizeof(s->pos_prob));
    
    int active_count = 0;
    for (int i = 0; i < s->count; i++) {
        if (!s->words[i].active) continue;
        active_count++;
        
        for (int j = 0; j < WORD_LEN; j++) {
            int idx = char_to_idx(s->words[i].word[j]);
            letter_freq[idx]++;
            s->pos_prob[j][idx]++;
        }
        
        char seen[ALPHA_SIZE] = {0};
        for (int j = 0; j < WORD_LEN; j++) {
            int idx = char_to_idx(s->words[i].word[j]);
            if (!seen[idx]) {
                letter_count[idx]++;
                seen[idx] = 1;
            }
        }
    }
    
    if (active_count == 0) return;
    
    for (int i = 0; i < ALPHA_SIZE; i++) {
        s->freq[i] = (double)letter_freq[i] / (active_count * WORD_LEN);
        double m_est = (letter_count[i] + s->freq[i] * active_count * s->bbq) / 
                       (active_count * s->bbq + active_count);
        s->emp_prob[i] = m_est;
        
        for (int j = 0; j < 5; j++) {
            s->pos_prob[j][i] /= active_count;
        }
    }
}

void filter_not_contains(Solver *s, char letter) {
    for (int i = 0; i < s->count; i++) {
        if (s->words[i].active && strchr(s->words[i].word, letter) == NULL) {
            s->words[i].active = 0;
        }
    }
}

void filter_contains(Solver *s, char letter) {
    for (int i = 0; i < s->count; i++) {
        if (s->words[i].active && strchr(s->words[i].word, letter) != NULL) {
            s->words[i].active = 0;
        }
    }
}

void filter_has_at_pos(Solver *s, char letter, int pos) {
    for (int i = 0; i < s->count; i++) {
        if (s->words[i].active && s->words[i].word[pos] == letter) {
            s->words[i].active = 0;
        }
    }
}

void filter_hasnt_at_pos(Solver *s, char letter, int pos) {
    for (int i = 0; i < s->count; i++) {
        if (s->words[i].active && s->words[i].word[pos] != letter) {
            s->words[i].active = 0;
        }
    }
}

void solve_step(Solver *s, const char *letters, const ColorState *colors) {
    for (int i = 0; i < WORD_LEN; i++) {
        char letter = tolower(letters[i]);
        int idx = char_to_idx(letter);
        
        if (!s->proved_letters[idx]) {
            s->proved_letters[idx] = 1;
        }
        
        if (colors[i] == GREEN) {
            filter_not_contains(s, letter);
            filter_hasnt_at_pos(s, letter, i);
            s->green_letters[idx] = 1;
            if (!s->good_letters[idx]) {
                s->good_letters[idx] = 1;
            }
        } else if (colors[i] == GREY) {
            if (!s->good_letters[idx]) {
                filter_contains(s, letter);
            }
        } else { // YELLOW
            filter_not_contains(s, letter);
            filter_has_at_pos(s, letter, i);
            if (!s->good_letters[idx]) {
                s->good_letters[idx] = 1;
            }
        }
    }
}

void choose_best_word(Solver *s, char *result) {
    calc_probabilities(s);
    
    int max_diversity = 0;
    int diverse_count = 0;
    int diverse_indices[WORD_COUNT];
    
    for (int i = 0; i < s->count; i++) {
        if (!s->words[i].active) continue;
        
        char seen[ALPHA_SIZE] = {0};
        int diversity = 0;
        for (int j = 0; j < WORD_LEN; j++) {
            int idx = char_to_idx(s->words[i].word[j]);
            if (!seen[idx] && !s->proved_letters[idx]) {
                diversity++;
                seen[idx] = 1;
            }
        }
        
        if (diversity > max_diversity) {
            max_diversity = diversity;
            diverse_count = 1;
            diverse_indices[0] = i;
        } else if (diversity == max_diversity) {
            diverse_indices[diverse_count++] = i;
        }
    }
    
    if (diverse_count == 0) {
        for (int i = 0; i < s->count; i++) {
            if (s->words[i].active) {
                strcpy(result, s->words[i].word);
                return;
            }
        }
        strcpy(result, "     ");
        return;
    }
    
    double best_score = -INFINITY;
    int best_idx = diverse_indices[0];
    
    for (int k = 0; k < diverse_count; k++) {
        int i = diverse_indices[k];
        double score = 0;
        
        for (int j = 0; j < WORD_LEN; j++) {
            int idx = char_to_idx(s->words[i].word[j]);
            if (!s->green_letters[idx]) {
                double emp = s->emp_prob[idx];
                double pos = s->pos_prob[j][idx];
                if (emp > 0 && pos > 0) {
                    score += log(emp * s->mayonnaise) + log(pos * s->ketchup);
                }
            }
        }
        
        if (score > best_score) {
            best_score = score;
            best_idx = i;
        }
    }
    
    strcpy(result, s->words[best_idx].word);
}

int get_active_count(Solver *s) {
    int count = 0;
    for (int i = 0; i < s->count; i++) {
        if (s->words[i].active) count++;
    }
    return count;
}

void draw_ui(WINDOW *win, const char guesses[][WORD_LEN+1], const ColorState colors[][WORD_LEN], 
             int current_row, int current_col, const char *suggestion, int remaining) {
    werase(win);
    box(win, 0, 0);
    
    mvwprintw(win, 1, 2, "WORDLE SOLVER - TUI Edition");
    mvwprintw(win, 2, 2, "==============================");
    mvwprintw(win, 4, 2, "Controls: Arrow keys=move, Space=cycle color, Enter=next row, Q=quit");
    mvwprintw(win, 5, 2, "Colors: Grey -> Yellow -> Green (Enter needs all 5 letters filled)");
    mvwprintw(win, 7, 2, "Your Guesses:");
    
    for (int row = 0; row < MAX_ATTEMPTS; row++) {
        mvwprintw(win, 9 + row * 2, 4, "Attempt %d: ", row + 1);
        
        for (int col = 0; col < WORD_LEN; col++) {
            char c = guesses[row][col] ? toupper(guesses[row][col]) : '_';
            
            if (row == current_row && col == current_col) {
                wattron(win, A_REVERSE);
            }
            
            // Show color even for empty cells if it's the current position or has a letter
            if (guesses[row][col] || (row == current_row && col == current_col)) {
                if (colors[row][col] == GREEN) {
                    wattron(win, COLOR_PAIR(COLOR_GREEN_PAIR));
                } else if (colors[row][col] == YELLOW) {
                    wattron(win, COLOR_PAIR(COLOR_YELLOW_PAIR));
                } else {
                    wattron(win, COLOR_PAIR(COLOR_GREY_PAIR));
                }
            }
            
            mvwprintw(win, 9 + row * 2, 16 + col * 2, "%c", c);
            
            wattroff(win, COLOR_PAIR(COLOR_GREY_PAIR));
            wattroff(win, COLOR_PAIR(COLOR_YELLOW_PAIR));
            wattroff(win, COLOR_PAIR(COLOR_GREEN_PAIR));
            wattroff(win, A_REVERSE);
        }
    }
    
    mvwprintw(win, 22, 2, "Suggested word: %s", suggestion[0] ? suggestion : "-----");
    mvwprintw(win, 23, 2, "Remaining words: %d", remaining);
    
    // Special display when only 1 word left
    if (remaining == 1 && suggestion[0]) {
        mvwprintw(win, 23, 25, " <- SOLUTION FOUND!");
    }
    
    wrefresh(win);
}

int main(void) {
    Solver solver;
    init_solver(&solver);
    
    char guesses[MAX_ATTEMPTS][WORD_LEN+1] = {0};
    ColorState colors[MAX_ATTEMPTS][WORD_LEN] = {0};
    int current_row = 0;
    int current_col = 0;
    char suggestion[WORD_LEN+1] = {0};
    
    choose_best_word(&solver, suggestion);
    
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);
    
    if (has_colors()) {
        start_color();
        init_pair(COLOR_GREY_PAIR, COLOR_WHITE, COLOR_BLACK);
        init_pair(COLOR_YELLOW_PAIR, COLOR_BLACK, COLOR_YELLOW);
        init_pair(COLOR_GREEN_PAIR, COLOR_BLACK, COLOR_GREEN);
    }
    
    WINDOW *win = newwin(UI_HEIGHT, UI_WIDTH, 0, 0);
    keypad(win, TRUE);
    
    int running = 1;
    while (running) {
        int remaining = get_active_count(&solver);
        draw_ui(win, guesses, colors, current_row, current_col, suggestion, remaining);
        
        int ch = wgetch(win);
        switch (ch) {
            case 'q':
            case 'Q':
                running = 0;
                break;
                
            case KEY_LEFT:
                if (current_col > 0) current_col--;
                break;
                
            case KEY_RIGHT:
                if (current_col < WORD_LEN - 1) current_col++;
                break;
                
            case KEY_UP:
                if (current_row > 0) current_row--;
                break;
                
            case KEY_DOWN:
                if (current_row < MAX_ATTEMPTS - 1) current_row++;
                break;
                
            case ' ':
                colors[current_row][current_col] = (colors[current_row][current_col] + 1) % 3;
                break;
                
            case '\n':
            case KEY_ENTER:
                // Check if we have a complete 5-letter word
                if (guesses[current_row][0] != '\0' && 
                    guesses[current_row][1] != '\0' &&
                    guesses[current_row][2] != '\0' &&
                    guesses[current_row][3] != '\0' &&
                    guesses[current_row][4] != '\0') {
                    solve_step(&solver, guesses[current_row], colors[current_row]);
                    choose_best_word(&solver, suggestion);
                    if (current_row < MAX_ATTEMPTS - 1) {
                        current_row++;
                        current_col = 0;
                        // Copy green letters to next row
                        for (int i = 0; i < WORD_LEN; i++) {
                            if (colors[current_row - 1][i] == GREEN) {
                                guesses[current_row][i] = guesses[current_row - 1][i];
                                colors[current_row][i] = GREEN;
                            }
                        }
                    }
                }
                break;
                
            default:
                if (isalpha(ch)) {
                    guesses[current_row][current_col] = tolower(ch);
                    // Ensure null termination
                    if (current_col < WORD_LEN) {
                        guesses[current_row][WORD_LEN] = '\0';
                    }
                    if (current_col < WORD_LEN - 1) {
                        current_col++;
                    }
                } else if (ch == KEY_BACKSPACE || ch == 127 || ch == '\b') {
                    if (current_col > 0) {
                        current_col--;
                    }
                    guesses[current_row][current_col] = '\0';
                }
                break;
        }
    }
    
    delwin(win);
    endwin();
    
    return 0;
}
