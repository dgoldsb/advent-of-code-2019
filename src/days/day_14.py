import typing
from collections import defaultdict
from copy import copy
from math import ceil

from aocd.models import Puzzle

import src.module.io  # set the session cookie

puzzle = Puzzle(year=2019, day=14)
inputs = puzzle.input_data.splitlines()


class Ingredient:
    def __init__(self, material, quantity):
        self.material = material
        self.quantity = quantity


class Recipe:
    def __init__(self, ingredients: typing.List[Ingredient], product: Ingredient):
        self.ingredients = ingredients
        self.product = product

    def get_materials_required(self, target_quantity):
        materials_required = defaultdict(lambda: 0)

        for ingredient in self.ingredients:
            material = ingredient.material
            if material != "ORE":
                div = ceil(target_quantity / self.product.quantity)
                materials_required[material] += div * ingredient.quantity

        return materials_required

    def get_ore_required(self, target_quantity):
        ore_required = 0

        for ingredient in self.ingredients:
            if ingredient.material == "ORE":
                div = ceil(target_quantity / self.product.quantity)
                ore_required += div * ingredient.quantity

        return ore_required


def build_recipe(line: str):
    ingredients_string, product_string = line.split(" => ")

    quantity, material = product_string.split(" ")
    product = Ingredient(material, int(quantity))

    ingredients = []
    for ingredient_string in ingredients_string.split(", "):
        quantity, material = ingredient_string.split(" ")
        ingredient = Ingredient(material, int(quantity))
        ingredients.append(ingredient)

    return Recipe(ingredients, product)


RECIPES = {build_recipe(l).product.material: build_recipe(l) for l in inputs}


def calculate_ore_required(fuel_quantity):
    stack = defaultdict(lambda: 0)
    stack["FUEL"] = fuel_quantity
    available_recipes = {"FUEL"}
    done_recipes = set()

    ore_counter = 0

    while True:
        loop_dict = copy(stack)

        for k, v in loop_dict.items():
            if v > 0 and k in available_recipes:
                # Set ore.
                ore_counter += RECIPES[k].get_ore_required(v)

                # Set other ingredients.
                for m, q in RECIPES[k].get_materials_required(v).items():
                    stack[m] += q

                # Set product to zero.
                stack[k] = 0

                # Mark this recipe as used.
                done_recipes.add(k)

                break
        else:
            break

        # Add to the set of available recipes.
        non_available_recipes = set()

        for k, v in RECIPES.items():
            if k not in done_recipes:
                for ingredient in v.ingredients:
                    non_available_recipes.add(ingredient.material)

        available_recipes = available_recipes.union(
            set(RECIPES.keys()) - non_available_recipes
        )

    return ore_counter


# PART 1

puzzle.answer_a = calculate_ore_required(1)


# PART 2


def binary_search(l, u, t, p):
    m = (u - l) // 2 + l

    ore = calculate_ore_required(m)
    print(f"{ore} ore for {m} fuel")

    if ore == t or p == ore:
        return m
    elif ore > t:
        return binary_search(l, m, t, ore)
    elif ore < t:
        return binary_search(m, u, t, ore)


target = 1000000000000
lower_bound = target // calculate_ore_required(1)
upper_bound = lower_bound * 2
puzzle.answer_b = binary_search(lower_bound, upper_bound, target, -1)
