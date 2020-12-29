from pathlib import Path
from functools import reduce
from collections import defaultdict

import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return lines


def parse_ingredients(lines):
    ingredient_lists = []

    for line in lines:
        elements = line.split()
        idx = elements.index("(contains")
        ingr = elements[:idx]
        allg = list(map(lambda s: s.strip(",)"), elements[idx+1:]))

        ingredient_lists.append({"ing": ingr, "all": allg})

    return ingredient_lists


def build_allg_ing_map(ingredient_lists):
    allg_ing_map = {}
    for ingr_list in ingredient_lists:
        for allg in ingr_list["all"]:
            if allg in allg_ing_map:
                allg_ing_map[allg] &= set(ingr_list["ing"])
            else:
                allg_ing_map[allg] = set(ingr_list["ing"])

    return allg_ing_map


def check_ingredients(ingredient_lists):
    allg_ing_map = build_allg_ing_map(ingredient_lists)

    all_ing = {ing for il in ingredient_lists for ing in il["ing"]}
    ingr_wo_allg = all_ing - {ing for allg in allg_ing_map for ing in allg_ing_map[allg]}
    ingr_with_allg = all_ing - ingr_wo_allg

    return ingr_wo_allg, ingr_with_allg


def all_allergenes_identified(allg_ing_map):
    return False if len(list(filter(lambda a: len(allg_ing_map[a]) > 1, allg_ing_map))) > 0 else True


def identify_allergenes(ingredient_lists):
    allg_ing_map = build_allg_ing_map(ingredient_lists)
    identified = set()

    while not all_allergenes_identified(allg_ing_map):

        for allg in allg_ing_map:
            if len(allg_ing_map[allg]) == 1:
                identified |= set(allg_ing_map[allg])
            else:
                allg_ing_map[allg] -= identified

    return map(lambda i: (i, list(allg_ing_map[i])[0]), allg_ing_map)


@app.command()
def part1(input_file: str):
    ingredient_lists = parse_ingredients(read_input_file(input_file))
    ingr_wo_allg, _ = check_ingredients(ingredient_lists)
    s = len(list(filter(lambda i: i in ingr_wo_allg,
            [ing for il in ingredient_lists for ing in il["ing"]])))

    print(f"Ingredient that cannot be allergenes appear {s} times.")


@app.command()
def part2(input_file: str):
    ingredient_lists = parse_ingredients(read_input_file(input_file))
    _, ingr_with_allg = check_ingredients(ingredient_lists)

    identified_allg = identify_allergenes(ingredient_lists)
    identified_allg = sorted(identified_allg, key=lambda i: i[0])
    canonical_list = ",".join([i[1] for i in identified_allg])

    print(f"The canonical dangerous ingredient list is: {canonical_list}")


if __name__ == "__main__":
    app()
