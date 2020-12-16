from pathlib import Path
from functools import reduce
import typer

DIRECTIONS = ["E", "S", "W", "N"]

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return list(map(lambda l: (l[0], int(l[1:])), lines))


def move(pos, step):
    operation, dist = step

    if operation in "WE":
        if operation == "W":
            dist *= -1
        new_pos = (pos[0], pos[1] + dist)

    if operation in "NS":
        if operation == "S":
            dist *= -1
        new_pos = (pos[0] + dist, pos[1])

    return new_pos


def turn_ship(direction, step):
    operation, dist = step

    if operation in "RL":
        if operation == "L":
            dist *= -1
        dir_index = DIRECTIONS.index(direction)
        new_dir_index = (dir_index + dist // 90) % 4
        return DIRECTIONS[new_dir_index]


def turn_waypoint(waypoint, step):
    operation, dist = step
    new_waypoint = waypoint

    if operation == "L":
        dist = 360 - dist

    turn_dir = (dist // 90) % 4

    if turn_dir == 1:
        new_waypoint = (waypoint[1] * -1, waypoint[0])
    elif turn_dir == 2:
        new_waypoint = (waypoint[0] * -1, waypoint[1] * -1)
    elif turn_dir == 3:
        new_waypoint = (waypoint[1], waypoint[0] * -1)

    return new_waypoint


def move_ship(ship, step):
    new_ship = dict()

    if step[0] == "F":
        step = (ship["dir"], step[1])

    if step[0] in DIRECTIONS:
        new_ship["pos"] = move(ship["pos"], step)
        new_ship["dir"] = ship["dir"]
    else:
        new_ship["pos"] = ship["pos"]
        new_ship["dir"] = turn_ship(ship["dir"], step)

    return new_ship


def move_ship_with_waypoint(ship, step):
    new_ship = dict()

    if step[0] == "F":
        new_ship["waypoint"] = ship["waypoint"]
        new_ship["pos"] = (ship["pos"][0] + step[1] * ship["waypoint"][0],
                           ship["pos"][1] + step[1] * ship["waypoint"][1])
    else:
        if step[0] in DIRECTIONS:
            new_ship["pos"] = ship["pos"]
            new_ship["waypoint"] = move(ship["waypoint"], step)
        else:
            new_ship["pos"] = ship["pos"]
            new_ship["waypoint"] = turn_waypoint(ship["waypoint"], step)

    return new_ship


@app.command()
def part1(input_file: str):
    ship = {"pos": (0, 0), "dir": "E"}
    r = reduce(lambda s, p: move_ship(s, p), read_input_file(input_file), ship)
    distance = abs(r["pos"][0]) + abs(r["pos"][1])
    print(f"The manhatten distance of the ships position is {distance}.")


@app.command()
def part2(input_file: str):
    ship = {"pos": (0, 0), "waypoint": (1, 10)}
    r = reduce(lambda s, p: move_ship_with_waypoint(s, p), read_input_file(input_file), ship)
    distance = abs(r["pos"][0]) + abs(r["pos"][1])
    print(f"The manhatten distance of the ships position is {distance}.")


if __name__ == "__main__":
    app()
