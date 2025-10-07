/* wordle_solver configuration */

/* Solver parameters - tune these for different solving strategies */
static const double BBQ = 1.5;         /* M-estimate smoothing parameter */
static const double KETCHUP = 1.56;    /* Position probability weight */
static const double MAYONNAISE = 0.84; /* Letter frequency weight */

/* UI colors (if terminal supports colors) */
static const int COLOR_GREY_PAIR = 1;
static const int COLOR_YELLOW_PAIR = 2;
static const int COLOR_GREEN_PAIR = 3;

/* UI dimensions */
static const int UI_WIDTH = 80;
static const int UI_HEIGHT = 25;
