# C TUI Implementation Summary

## Overview
This is a suckless, fast, and ultra-optimized C implementation of the Wordle solver with a Text User Interface (TUI). It mirrors the Python version's algorithm while being significantly more efficient.

## What Was Created

### Core Files
1. **wordle_solver.c** (374 lines)
   - Main solver algorithm implementation
   - TUI interface using ncurses
   - All logic in a single file (suckless principle)

2. **words.h** (12,972 words)
   - Generated from Python word list
   - Static const array for fast access
   - No runtime file I/O needed

3. **config.h**
   - Suckless-style configuration
   - Tunable solver parameters (BBQ, KETCHUP, MAYONNAISE)
   - UI settings (colors, dimensions)

4. **Makefile**
   - POSIX-compliant build system
   - Optimization flags (-O3 -march=native)
   - Standard targets (all, clean, install, uninstall)

5. **QUICKREF.md**
   - Quick reference guide
   - Keyboard controls
   - Algorithm explanation

### Documentation Updates
- Updated README.md with C version instructions
- Added build requirements and instructions
- Documented suckless principles followed

## Technical Details

### Algorithm Fidelity
The C implementation exactly replicates the Python algorithm:
- Letter frequency analysis with M-estimate smoothing
- Positional probability calculation
- Diversity-based word selection
- Weighted scoring combining frequency and position

### Performance Characteristics
- Binary size: ~500KB (self-contained)
- Compilation: O3 optimizations + native CPU instructions
- Memory: Static allocation, no dynamic memory management
- Speed: Instant suggestions even with 12,972 words

### Suckless Principles Applied
1. ✅ Single-file implementation
2. ✅ Configuration via header file
3. ✅ Minimal external dependencies
4. ✅ Simple, readable code
5. ✅ No unnecessary features
6. ✅ Fast and efficient

## Usage

### Build
```bash
make
```

### Run
```bash
./wordle_solver
```

### Customize
Edit `config.h` to change:
- Solver parameters (BBQ, KETCHUP, MAYONNAISE)
- UI colors and dimensions

## Comparison with Python Version

| Aspect | Python Version | C TUI Version |
|--------|---------------|---------------|
| Runtime | Interpreted | Native binary |
| Dependencies | toga, Python 3.x | ncurses only |
| Size | ~16KB + Python | ~500KB standalone |
| Speed | Good | Excellent |
| Interface | GUI (toga) | TUI (ncurses) |
| Portability | Needs Python | Single binary |
| Configuration | Code edits | config.h |

## Files Added to Repository
- wordle_solver.c
- words.h
- config.h  
- Makefile
- QUICKREF.md
- Updated README.md
- Updated .gitignore

## Testing
The implementation was tested with:
- Compilation with no warnings (gcc -Wall -Wextra)
- Algorithm verification against Python version
- Dependency verification (ldd)
- Build system verification (make clean && make)
