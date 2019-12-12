import math
from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=12)
inputs = aoc.ints(puzzle.input_data)


class Planet:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    @property
    def total_energy(self):
        return sum([abs(x) for x in self.position]) * sum([abs(x) for x in self.velocity])


class System:
    def __init__(self, planets):
        self.planets = planets
        self.initial_state = copy(planets)

    @property
    def total_energy(self):
        return sum([planet.total_energy for planet in self.planets])

    def find_period(self, dim):
        self.planets = copy(self.initial_state)

        target_p = [x.position[dim] for x in self.planets]
        target_v = [x.velocity[dim] for x in self.planets]

        counter = 0
        while True:
            self._apply_gravity()
            self._apply_velocity()
            counter += 1

            if [x.position[dim] for x in self.planets] == target_p and \
                    [x.velocity[dim] for x in self.planets] == target_v:
                break

        print(f"Found period {counter} for {dim}")
        return counter

    def run(self, steps):
        self.planets = copy(self.initial_state)

        for _ in range(steps):
            self._apply_gravity()
            self._apply_velocity()

    def _apply_gravity(self):
        for a in self.planets:
            for b in self.planets:
                for dim in range(3):
                    if a.position[dim] > b.position[dim]:
                        a.velocity[dim] -= 1
                    elif a.position[dim] < b.position[dim]:
                        a.velocity[dim] += 1

    def _apply_velocity(self):
        for planet in self.planets:
            for dim in range(3):
                planet.position[dim] += planet.velocity[dim]


system = System([Planet(inputs[(i * 3):(i * 3) + 3]) for i in range(4)])


# PART 1

system.run(1000)
puzzle.answer_a = system.total_energy


# PART 2

periods = [system.find_period(0), system.find_period(1), system.find_period(2)]


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


first_lcm = lcm(*periods[0:2])
puzzle.answer_b = lcm(first_lcm, periods[2])

