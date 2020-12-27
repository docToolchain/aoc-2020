from pathlib import Path
from functools import reduce
from copy import deepcopy

import re
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    tiles = dict()
    for l in lines:
        if "Tile" in l:
            key = int(l[5:9])
            tiles[key] = []
        else:
            if l.strip() != "":
                tiles[key].append(l.strip())

    return tiles


def borders(tile):
    l = ""
    r = ""
    for i in range(len(tile)):
        l += tile[i][0]
        r += tile[i][-1]

    return [tile[0], tile[-1], l, r]


def all_borders(tiles):
    return reduce(lambda l, k: l + borders(tiles[k]), tiles, [])


def flip_and_turn(borders):
    return reduce(lambda r, b: r + [b[::-1]], borders, borders)


def count_common_borders(key, tiles):
    tile_borders = flip_and_turn(borders(tiles[key]))

    other_tiles = deepcopy(tiles)
    del other_tiles[key]
    other_borders = all_borders(other_tiles)

    return reduce(lambda s, b: s + 1 if b in other_borders else s, tile_borders, 0)


@app.command()
def part1(input_file: str):
    tiles = read_input_file(input_file)
    common_borders = map(lambda k: (k, count_common_borders(k, tiles)), tiles)
    r = reduce(lambda p, e: p * e[0], filter(lambda e: e[1] == 2, common_borders), 1)

    print(f"The product of the IDs of the four corner tiles is {r}")

if __name__ == "__main__":
    app()
