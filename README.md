# PyWordle GUI

## Python GUI Version

### Requirements

`pip install --pre toga` or `python3 -m pip install --pre toga` 

### How to use it

`python3 gui.py`

### How it works

Just input your word and the corresponding colors and the program will solve it for you.

Watch this video for a demonstration:

https://user-images.githubusercontent.com/31370059/150675258-08326958-7878-4fb6-8600-dab2c30a83b7.mp4

Updated demonstration with a particularly difficult case (and me trying to explain what the program *actually* does):

https://user-images.githubusercontent.com/31370059/152317278-a85b38fd-02b1-4dd6-8770-867a0d822455.mp4

## C TUI Version (Fast & Optimized)

A suckless, fast, and ultra-optimized C implementation with a Text User Interface (TUI).

### Requirements

- GCC or compatible C compiler
- ncurses library
- make

On Debian/Ubuntu:
```bash
sudo apt-get install build-essential libncurses-dev
```

On macOS:
```bash
brew install ncurses
```

### Building

```bash
make
```

### Running

```bash
./wordle_solver
```

### How to use the TUI

1. Use **arrow keys** to navigate between letter positions
2. Type letters directly to fill in your guess
3. Press **Space** to cycle through colors (Grey -> Yellow -> Green)
4. Press **Enter** to submit the current row and get a new suggestion
5. Press **Q** to quit

The program will suggest the most probable word based on your input and display the number of remaining possible words.

### Performance

The C version is highly optimized with:
- O3 compiler optimizations
- Native CPU architecture optimizations
- Efficient probability calculations
- Fast word filtering algorithms
- Minimal memory footprint (~500KB binary)

