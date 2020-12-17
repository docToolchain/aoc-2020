from pathlib import Path
from functools import reduce
import typer


ACTIVE = "#"
INACTIVE = "."


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return list(map(lambda l: l.strip(), lines))


def parse_grid(lines, dim=3):
    if dim == 3:
        grid = init_empty_grid(len(lines), len(lines[0]), 1, 0)
    else:
        grid = init_empty_grid(len(lines), len(lines[0]), 1, 1)

    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == ACTIVE:
                if dim == 3:
                    grid[i][j][0] = ACTIVE
                else:
                    grid[i][j][0][0] = ACTIVE

    return grid


def init_empty_grid(size_x, size_y, size_z, size_w):
    if size_w == 0:
        return [[[
            INACTIVE for _ in range(size_z)]
            for _ in range(size_y)]
            for _ in range(size_x)]
    else:
        return [[[[
            INACTIVE for _ in range(size_w)]
            for _ in range(size_w)]
            for _ in range(size_y)]
            for _ in range(size_x)]


def neighbour_coordinates(coordinate):
    if len(coordinate) == 3:
        x, y, z = coordinate
        coordinates = [(a, b, c)
                       for a in range(x-1, x+2)
                       for b in range(y-1, y+2)
                       for c in range(z-1, z+2)]
    else:
        x, y, z, w = coordinate
        coordinates = [(a, b, c, d)
                       for a in range(x-1, x+2)
                       for b in range(y-1, y+2)
                       for c in range(z-1, z+2)
                       for d in range(w-1, w+2)]

    coordinates.remove(coordinate)
    return coordinates


def active_neighbours(coordinate, grid):
    coordinates = neighbour_coordinates(coordinate)
    active = reduce(lambda s, c: s + 1 if cell_state(c, grid) == ACTIVE else s, coordinates, 0)
    return active


def all_coordinates(grid):
    coordinates = []
    if type(grid[0][0][0]) is list:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                for z in range(len(grid[x][y])):
                    for w in range(len(grid[x][y][z])):
                        coordinates.append((x, y, z, w))
    else:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                for z in range(len(grid[x][y])):
                    coordinates.append((x, y, z))
    return coordinates


def active_cell_coordinates(grid):
    return list(filter(lambda c: cell_state(c, grid) == ACTIVE, all_coordinates(grid)))


def cell_state(coordinate, grid):
    if len(coordinate) == 3:
        x, y, z = coordinate
        if x < 0 or y < 0 or z < 0:
            state = INACTIVE
        elif x >= len(grid) or y >= len(grid[0]) or z >= len(grid[0][0]):
            state = INACTIVE
        else:
            state = grid[x][y][z]
    else:
        x, y, z, w = coordinate
        if x < 0 or y < 0 or z < 0 or w < 0:
            state = INACTIVE
        elif x >= len(grid) or y >= len(grid[0]) or z >= len(grid[0][0]) or w >= len(grid[0][0][0]):
            state = INACTIVE
        else:
            state = grid[x][y][z][w]

    return state


def execute_step(grid):
    '''
    Calculates the new state of the grid based on the following rules:
    - If a cell is active and exactly 2 or 3 of its neighbors are also active,
      the cube remains active. Otherwise, the cell becomes inactive.
    - If a cell is inactive but exactly 3 of its neighbors are active,
      the cell becomes active.
    '''

    if type(grid[0][0][0]) is list:
        new_grid = init_empty_grid(
            len(grid) + 2, len(grid[0]) + 2, len(grid[0][0]) + 2, len(grid[0][0][0]) +2)
    else:
        new_grid = init_empty_grid(
            len(grid) + 2, len(grid[0]) + 2, len(grid[0][0]) + 2, 0)

    for c in all_coordinates(new_grid):
        if len(c) == 3:
            old_coordinate = (c[0]-1, c[1]-1, c[2]-1)
        else:
            old_coordinate = (c[0]-1, c[1]-1, c[2]-1, c[3]-1)

        state = cell_state(old_coordinate, grid)
        active_neighbours_count = active_neighbours(old_coordinate, grid)

        if (state == ACTIVE and active_neighbours_count in [2, 3])\
           or (state == INACTIVE and active_neighbours_count == 3):
            if len(c) == 3:
                new_grid[c[0]][c[1]][c[2]] = ACTIVE
            else:
                new_grid[c[0]][c[1]][c[2]][c[3]] = ACTIVE

    return new_grid


@app.command()
def part1(input_file: str):
    grid = parse_grid(read_input_file(input_file))
    for _ in range(6):
        grid = execute_step(grid)
    print(f"After six cycles {len(active_cell_coordinates(grid))} cubes are active.")


@app.command()
def part2(input_file: str):
    grid = parse_grid(read_input_file(input_file), 4)
    for _ in range(6):
        grid = execute_step(grid)
    print(f"After six cycles {len(active_cell_coordinates(grid))} cubes are active.")


if __name__ == "__main__":
    app()
