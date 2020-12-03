from pathlib import Path
from functools import reduce
import typer


TREE = '#'

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    lines = list(map(lambda s: s.strip(), lines))
    return lines


def calculate_coordinates(x_steps, y_steps, toboggan_map):
    return list(
            map(
                lambda e: (e[1], (y_steps * e[0]) % len(toboggan_map[0])),
                enumerate(range(0, len(toboggan_map), x_steps))))


def is_tree_at_position(x, y, toboggan_map):
    return toboggan_map[x][y] == TREE


def count_trees(x_steps, y_steps, toboggan_map):
    count = reduce(
            lambda s, c: s + 1 if is_tree_at_position(c[0], c[1], toboggan_map) else s,
            calculate_coordinates(x_steps, y_steps, toboggan_map),
            0)
    return count


@app.command()
def part1(input_file: str):
    toboggan_map = read_input_file(input_file)
    number_of_trees = count_trees(1, 3, toboggan_map)
    print(f"The number of trees on the trajectory is {number_of_trees}")


@app.command()
def part2(input_file: str):
    toboggan_map = read_input_file(input_file)

    result = count_trees(1, 1, toboggan_map)
    result *= count_trees(1, 3, toboggan_map)
    result *= count_trees(1, 5, toboggan_map)
    result *= count_trees(1, 7, toboggan_map)
    result *= count_trees(2, 1, toboggan_map)

    print(f"The product of the number of trees on the trajectories is {result}")


if __name__ == "__main__":
    app()
