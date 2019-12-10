from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=10)
inputs = puzzle.input_data.splitlines()

all_asteroids = set()

for y, row in enumerate(inputs):
    for x, field in enumerate(row):
        if field == "#":
            all_asteroids.add((x, y))


# PART 1

def get_visible_angles(asteroid, asteroids):
    visible = set()

    for a in asteroids:
        try:
            # Could make this faster by counting for both asteroids.
            visible.add(aoc.compute_angle(asteroid, a))
        except ValueError:
            continue

    return visible


largest_number_visible = 0
station = None
for a in all_asteroids:
    angles = get_visible_angles(a, all_asteroids)
    if len(angles) > largest_number_visible:
        largest_number_visible = len(angles)
        station = a

puzzle.answer_a = largest_number_visible


# PART 2

def find_target(angle, asteroid, asteroids):
    lowest_distance = None
    closest = None

    for a in asteroids:
        if aoc.compute_angle(asteroid, a) == angle:
            if lowest_distance is None or aoc.manhattan(asteroid, a) < lowest_distance:
                lowest_distance = aoc.manhattan(asteroid, a)
                closest = a

    return closest


# Remove the station to avoid destroying that one.
all_asteroids.remove(station)

destroy_counter = 0
destroy_angles = []
while True:
    if not destroy_angles:
        destroy_angles = sorted(get_visible_angles(station, all_asteroids))

    destroy_angle = destroy_angles.pop(0)
    destroy_target = find_target(destroy_angle, station, all_asteroids)
    all_asteroids.remove(destroy_target)

    destroy_counter += 1
    if destroy_counter == 200:
        puzzle.answer_b = destroy_target[0] * 100 + destroy_target[1]
        break
