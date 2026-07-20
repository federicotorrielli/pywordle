# wordle-solver

`wordle-solver` is a terminal program that narrows a bundled dictionary from
Wordle feedback and suggests the next guess. It is written in C and uses
ncurses for the interface.

## Build

You need a C99 compiler, `make`, and the ncurses development files.

On Debian or Ubuntu:

```sh
sudo apt install build-essential libncurses-dev
```

On macOS with Homebrew:

```sh
brew install ncurses
```

Build and run the program:

```sh
make
./wordle-solver
```

Run the solver tests with:

```sh
make test
```

## Controls

- Type a letter to fill the selected tile.
- Use Left and Right to move between tiles.
- Press Space to cycle a tile through grey, yellow, and green.
- Press Enter to submit a complete guess.
- Press Backspace to clear a tile.
- Press Escape to quit.

The terminal must be at least 80 columns wide and 24 rows high.

## Solver

The bundled dictionary contains 12,972 five letter words. After each guess,
the solver computes the feedback that every remaining candidate would have
produced. A candidate remains only when its feedback exactly matches the
submitted feedback. This rule handles repeated letters without special cases.

The next guess is selected from the remaining candidates. The solver first
prefers words with more untested letters, then ranks tied words by letter and
position frequency. The two weights are defined in `config.h`.

This filtering rule follows the hard mode principle described by Chao-Lin Liu
in [Using Wordle for Learning to Design and Compare Strategies](https://arxiv.org/abs/2205.11225).

## Installation

```sh
sudo make install
```

Set `PREFIX` to install elsewhere. `DESTDIR` is also supported for packaging.

## Authors and licence

Copyright 2022 to 2026 Federico Torrielli and Lorenzo Sciandra.

The project is licensed under the European Union Public Licence v. 1.2 only.
The complete terms are in [LICENSE](LICENSE).
