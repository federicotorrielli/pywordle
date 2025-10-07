# C TUI Wordle Solver - Quick Reference

## Building & Running
```bash
make              # Build the solver
./wordle_solver   # Run the TUI application
make clean        # Clean build artifacts
```

## Keyboard Controls
- **Arrow Keys** - Navigate between letter positions
- **A-Z** - Enter letters
- **Backspace** - Delete letter
- **Space** - Cycle color (Grey → Yellow → Green)
- **Enter** - Submit guess and get next suggestion
- **Q** - Quit application

## Color Meanings (Wordle Standard)
- **Grey** - Letter not in word
- **Yellow** - Letter in word, wrong position
- **Green** - Letter in word, correct position

## Customization
Edit `config.h` to tune solver parameters:
- Adjust BBQ, KETCHUP, MAYONNAISE for different solving strategies
- Modify UI colors and dimensions

## Algorithm
The solver uses:
1. Letter frequency analysis across remaining words
2. Positional probability calculations
3. M-estimate smoothing for probability estimation
4. Diversity-based word selection
5. Weighted scoring combining frequency and position data

## Files
- `wordle_solver.c` - Main implementation (374 lines)
- `config.h` - Configuration parameters
- `words.h` - Word dictionary (12,972 words)
- `Makefile` - Build configuration
