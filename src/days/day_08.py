from aocd.models import Puzzle

import src.module.io  # set the session cookie

puzzle = Puzzle(year=2019, day=8)
inputs = [int(x) for x in puzzle.input_data]


WIDTH = 25
HEIGHT = 6
LAYERS = len(inputs) // (WIDTH * HEIGHT)


image = []
for layer in range(LAYERS):
    start = layer * WIDTH * HEIGHT
    end = (layer + 1) * WIDTH * HEIGHT
    layer = inputs[start:end]
    image.append(layer)


# PART 1

least_zeroes = WIDTH * HEIGHT
corruption_check = 0
for layer in image:
    if layer.count(0) < least_zeroes:
        least_zeroes = layer.count(0)
        corruption_check = layer.count(1) * layer.count(2)

puzzle.answer_a = corruption_check


# PART 2

output_layer = []


def coalesce(c, n):
    if c == 2:
        return n
    else:
        return c


for pixel in range(WIDTH * HEIGHT):
    pixel_value = 2
    for layer in image:
        pixel_value = coalesce(pixel_value, layer[pixel])
    output_layer.append(pixel_value)

for row in range(HEIGHT):
    start = row * WIDTH
    end = (row + 1) * WIDTH
    print(output_layer[start:end])
