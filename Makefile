.POSIX:

CC = cc
CFLAGS = -O2 -Wall -Wextra -Wpedantic -std=c99
LDFLAGS =
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin

PROGRAM = wordle-solver
OBJECTS = wordle_solver.o solver.o
TEST_PROGRAM = test-solver
TEST_OBJECTS = test_solver.o solver.o

all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS) -lncurses -lm

$(TEST_PROGRAM): $(TEST_OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(TEST_OBJECTS) -lm

wordle_solver.o: wordle_solver.c solver.h config.h
solver.o: solver.c solver.h config.h words.h
test_solver.o: test_solver.c solver.h

test: $(TEST_PROGRAM)
	./$(TEST_PROGRAM)

clean:
	rm -f $(PROGRAM) $(TEST_PROGRAM) $(OBJECTS) test_solver.o

install: $(PROGRAM)
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 $(PROGRAM) $(DESTDIR)$(BINDIR)/$(PROGRAM)

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/$(PROGRAM)

.PHONY: all clean install test uninstall
