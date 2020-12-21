#!/usr/bin/env python3
import os
from collections import defaultdict
from itertools import chain
from typing import Dict, Set


class Solver:
    def __init__(self, filepath: str) -> None:
        with open(filepath, 'r') as text_file:
            self.lines = [line.rstrip() for line in text_file.readlines()]
        # foods: "string of ingredients" -> set of allergens
        self.foods = {}  # type: Dict[str, Set[str]]
        # ingredients: ingredient -> set of foods it is in
        self.ingredients = defaultdict(set)  # type: Dict[str, Set[str]]
        # allergens: allergen -> set of foods it is in
        self.allergens = defaultdict(set)  # type: Dict[str, Set[str]]
        # possibilities: allergen -> set of ingredients it might be in
        self.possibilities = {}  # type: Dict[str, Set[str]]
        # dangers: ingredient -> allergen it contains
        self.dangers = {}  # type: Dict[str, str]

    @staticmethod
    def get_food_ingredients(food: str) -> Set[str]:
        """Return the ingredients from the string representing the food."""
        return set(food.split())

    def parse_foods(self) -> None:
        """Parse the input lines and structure the data by foods, ingredients, and allergens."""
        for line in self.lines:
            food, allergens_string = line.replace(')', '').split(" (contains ", maxsplit=1)
            ingredients = self.get_food_ingredients(food)
            allergens = set(allergens_string.split(", "))
            self.foods[food] = allergens
            for ingredient in ingredients:
                self.ingredients[ingredient].add(food)
            for allergen in allergens:
                self.allergens[allergen].add(food)

    def initialize_possibilities(self, allergen: str) -> None:
        """Determine which ingredients allergen might be in."""
        foods = self.allergens[allergen]
        if len(foods) == 1:
            # An allergen in only one food must be in one of its ingredients.
            self.possibilities[allergen] = self.get_food_ingredients(next(iter(foods)))
        else:
            # An allergen must be in one of the ingredients which is in all foods containing this allergen.
            ingredients = set(chain.from_iterable(self.get_food_ingredients(food) for food in foods))
            self.possibilities[allergen] = {ingredient for ingredient in ingredients if self.ingredients[ingredient].intersection(foods) == foods}

    def handle_danger(self, ingredient: str, allergen: str) -> None:
        """Mark ingredient as containing allergen, and remove it from the possibilities of all other allergens."""
        self.dangers[ingredient] = allergen
        del self.possibilities[allergen]
        for check_ingredients in self.possibilities.values():
            if ingredient in check_ingredients:
                check_ingredients.remove(ingredient)

    def solve_part1(self) -> int:
        self.parse_foods()
        for allergen in self.allergens:
            self.initialize_possibilities(allergen)
        # these_ingredients: ingredients possibly containing an allergen
        these_ingredients = set(chain.from_iterable(ingredients for ingredients in self.possibilities.values()))
        # those_ingredients: ingredients not possibly containing any allergen
        those_ingredients = set(self.ingredients.keys()).difference(these_ingredients)
        appearance_count = sum([len(self.ingredients[ingredient]) for ingredient in those_ingredients])
        return appearance_count

    def solve_part2(self) -> str:
        self.solve_part1()
        # Eliminate possibilities by resolving ingredients being a single possibility for an allergen.
        while self.possibilities:
            for allergen, ingredients in list(self.possibilities.items()):
                if len(ingredients) == 1:
                    self.handle_danger(ingredients.pop(), allergen)
        dangers = list(self.dangers.items())
        dangers.sort(key=lambda danger: danger[1])
        dangerous_ingredients = ','.join(danger[0] for danger in dangers)
        return dangerous_ingredients


if __name__ == "__main__":
    solver = Solver(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
