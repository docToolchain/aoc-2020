from pathlib import Path
from functools import reduce

import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    lines = list(map(lambda l: l.strip(), lines))
    idx = lines.index("")

    p1 = list(map(lambda l: int(l), lines[1:idx]))
    p2 = list(map(lambda l: int(l), lines[idx+2:]))

    return p1, p2


def game_ended(p1, p2, end_game=False):
    if end_game:
        return True
    else:
        return len(p1) == 0 or len(p2) == 0


def play_round(p1, p2):
    c1, *new_p1 = p1
    c2, *new_p2 = p2

    if c1 > c2:
        new_p1 += [c1, c2]
    else:
        new_p2 += [c2, c1]

    return new_p1, new_p2


def play_combat(p1, p2):
    while not game_ended(p1, p2):
        p1, p2 = play_round(p1, p2)
    return p1, p2


def play_recursive_combat(p1, p2):
    end_game = False
    previous_decks = {"p1": [], "p2": []}

    while not game_ended(p1, p2, end_game):
        p1, p2, end_game, previous_decks = play_recursive_round(p1, p2, previous_decks)

    if len(p2) == 0 or end_game:
        winner = "p1"
    else:
        winner = "p2"

    return p1, p2, winner


def play_recursive_round(p1, p2, previous_decks):
    if p1 in previous_decks["p1"] or p2 in previous_decks["p2"]:
        return p1, p2, True, previous_decks
    else:
        previous_decks["p1"].append(p1)
        previous_decks["p2"].append(p2)

        c1, *new_p1 = p1
        c2, *new_p2 = p2

        if c1 <= len(new_p1) and c2 <= len(new_p2):
            p1, p2, winner = play_recursive_combat(new_p1[:c1], new_p2[:c2])
            if winner == "p1":
                new_p1 += [c1, c2]
            else:
                new_p2 += [c2, c1]
        else:
            new_p1, new_p2 = play_round(p1, p2)

        return new_p1, new_p2, "", previous_decks


def calculate_score(deck):
    return reduce(lambda s, e: s + e[0] * e[1], enumerate(reversed(deck), 1), 0)


@app.command()
def part1(input_file: str):
    p1, p2 = read_input_file(input_file)
    p1, p2 = play_combat(p1, p2)

    if len(p1) > 0:
        score = calculate_score(p1)
    else:
        score = calculate_score(p2)

    print(f"The winnig score for the game is {score}.")


@app.command()
def part2(input_file: str):
    p1, p2 = read_input_file(input_file)
    p1, p2, _ = play_recursive_combat(p1, p2)

    if len(p1) > 0:
        score = calculate_score(p1)
    else:
        score = calculate_score(p2)

    print(f"Player 1's deck: {p1}")
    print(f"Player 2's deck: {p2}")
    print(f"The winnig score for the game of recursive combat is {score}.")


if __name__ == "__main__":
    app()
