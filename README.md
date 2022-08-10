# figure-game-solver

A solver for [figure.game](https://figure.game/).

This is pure brute force and as such is guaranteed to find an
optimal solution (with the minimum possible number of moves) for
each puzzle. Because of optimizations, it does not prove uniqueness
of these solutions.

Usage:

    python solve.py game.fg

## Game file format

I made this rather simple and arbitrary format to store games
because I don't know of any official one.

    Title: Figure #43
    Limit: 9
    YBBBB
    PWBYW
    YBYWY
    BPWBY
    YYWYY

The title can be anything, and the limit is self-explanatory.

The game board is represented exactly how it is shown on the page
to a human player. Each letter represents either the first letter of
a color or the first letter of the shape corresponding to tiles of
that color. As of this writing, figure.game boards use the following
colors and shapes:

    Blue = Diamond
    Pink = Triangle
    White = Square
    Yellow = Circle

## Solution speed

This solver is pretty fast!

    % time python solve.py game43.fg
    Figure #43
    Game solved in 9 moves.
    Solution: 5 4 4 2 1 1 3 5 3
    python solve.py game43.fg  0.53s user 0.00s system 99% cpu 0.536 total

