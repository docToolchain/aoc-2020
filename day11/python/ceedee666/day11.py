from pathlib import Path
from functools import reduce
from itertools import chain
from collections import Counter

import typer

EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return list(map(lambda l: list(l.strip()), lines))


def pos_in_grid(pos, grid):
    x_size = len(grid)
    y_size = len(grid[0])

    return pos[0] >= 0 and pos[1] >= 0 \
           and pos[0] < x_size and pos[1] < y_size


def check_line_of_sight(index, pos, grid):
    delta_x = index[0] - pos[0]
    delta_y = index[1] - pos[1]

    state = grid[index[0]][index[1]]
    next_in_los = (index[0] + delta_x, index[1] + delta_y) 
    
    while state not in [OCCUPIED, EMPTY] and pos_in_grid(next_in_los, grid):
        index = next_in_los
        state = grid[index[0]][index[1]]
        next_in_los = (index[0] + delta_x, index[1] + delta_y)

    return index


def neighbor_indicies(pos, grid, neighbor_rules):
    indices = [(x, y) for x in range(pos[0]-1, pos[0]+2)
                      for y in range(pos[1]-1, pos[1]+2)]
    indices.remove(pos)
    indices = list(
                filter(
                    lambda p: pos_in_grid(p, grid), indices))

    if neighbor_rules == 1:
        indices = map(lambda i: check_line_of_sight(i, pos, grid), indices)

    return indices

def occupied_neighbors(pos, grid, neighbor_rules):
    neighbors = neighbor_indicies(pos, grid, neighbor_rules)
    return reduce(
            lambda a, n: a + 1 if grid[n[0]][n[1]] == OCCUPIED else a,
            neighbors, 0)


def next_state(pos, grid, max_occ_seats, neighbor_rules):
    state = grid[pos[0]][pos[1]]

    if state == FLOOR:
        return FLOOR
    elif state == EMPTY and occupied_neighbors(pos, grid, neighbor_rules) == 0:
        return OCCUPIED
    elif state == OCCUPIED and \
        occupied_neighbors(pos, grid, neighbor_rules) >= max_occ_seats:
        return EMPTY
    else:
        return state


def simulate_step(grid, max_occ_seats=4, neighbor_rules=0):
    next_grid = []
    for x in range(len(grid)):
        next_row = []
        for y in range(len(grid[0])):
            next_row.append(next_state((x, y), grid, max_occ_seats, neighbor_rules))
        next_grid.append(next_row)
    return next_grid


def simulator(start_grid, max_occ_seats=4, neighbor_rules=0):
    current = start_grid
    while True:
        current = simulate_step(current, max_occ_seats, neighbor_rules)
        yield current


@app.command()
def part1(input_file: str):
    previous_grid = []
    current_grid = read_input_file(input_file)
    sim = simulator(current_grid)

    while current_grid != previous_grid:
        previous_grid = current_grid
        current_grid = next(sim)

    counter = Counter(chain.from_iterable(current_grid))

    print(f"The number of occupied seats is {counter[OCCUPIED]}")


@app.command()
def part2(input_file: str):
    previous_grid = []
    current_grid = read_input_file(input_file)
    sim = simulator(current_grid, 5, 1)

    while current_grid != previous_grid:
        previous_grid = current_grid
        current_grid = next(sim)

    counter = Counter(chain.from_iterable(current_grid))

    print(f"The number of occupied seats is {counter[OCCUPIED]}")


if __name__ == "__main__":
    app()
