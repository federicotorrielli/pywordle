.POSIX:
CC = gcc
CFLAGS = -O3 -Wall -Wextra -std=c99 -march=native
LDFLAGS = -lncurses -lm
TARGET = wordle_solver
SRC = wordle_solver.c

all: $(TARGET)

$(TARGET): $(SRC) words.h config.h
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)

install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/

uninstall:
	rm -f /usr/local/bin/$(TARGET)

.PHONY: all clean install uninstall
