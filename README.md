# Advent of Code 2019

Santa has become stranded at the edge of the Solar System while delivering presents to other planets! To accurately calculate his position in space, safely align his warp drive, and return to Earth in time to save Christmas, he needs you to bring him measurements from fifty stars.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

## Introduction

This year, I aimed to challenge myself to keep up with the Advent of Code the best I could, doing assignments on the day itself as much as possible.
In addition, I wanted to only use standard libraries, and being better about writing clean code than last year, making code common in `aoc.py` whenever possible.

I came back to this year a few years later, finishing the remaining challenges.
I see a lot of room for cleaner and faster solutions, but for now I will leave this as is and focus on different puzzles.

## Quick start

All solutions import the `aoc.py` file for common functions.
Upon importing this file, a file `session_cookie` is expected in the root of this repository.
This file should contain the session cookie that the Advent of Code website provides you after authenticating. Using this cookie, inputs are automatically fetched, and in some cases solutions are automatically submitted.
The only dependency for this project is `advent-of-code-data`, the Python version used is `3.7`.

## TODO

- [ ] Speed up day 15
- [ ] Day 16 without numpy
- [ ] Speed up day 19
- [ ] Do proper signaling in the async code. Practicing async was nice at the time, but I wrote the original without using the synchronisation primitives.
