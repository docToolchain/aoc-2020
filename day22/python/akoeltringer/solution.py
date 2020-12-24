#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 22"""

# stdlib imports
from typing import Tuple, List, Optional

# 3rd party lib imports

# own stuff
import utils


T_DECK = List[int]
T_GAME = Tuple[T_DECK, List[int]]


def parse_input(input_raw: str) -> T_GAME:
    p1_raw, p2_raw = input_raw.strip().split("\n\n")

    # left is top!
    p1 = [int(e) for e in p1_raw.split("\n")[1:]]
    p2 = [int(e) for e in p2_raw.split("\n")[1:]]

    return p1, p2


def play_game(p1: T_DECK, p2: T_DECK):

    while len(p1) > 0 and len(p2) > 0:
        c1, c2 = p1.pop(0), p2.pop(0)

        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        elif c1 < c2:
            p2.append(c2)
            p2.append(c1)
        else:
            raise ValueError("something weird happened (tie!)")

    p_winner = p1 if len(p1) > 0 else p2
    score = sum([a * b for a, b in zip(p_winner, range(len(p_winner), 0, -1))])
    return score


def play_game_recursive(player1: T_DECK, player2: T_DECK):
    def recurse(p1: T_DECK, p2: T_DECK) -> Tuple[Optional[bool], Optional[T_DECK]]:
        """play the recursion, return a bool (True = player 1 won) and the winning deck"""
        history = []

        while len(p1) > 0 and len(p2) > 0:
            # prevent infinite loops
            if (p1, p2) in history:
                return True, None

            history.append((p1.copy(), p2.copy()))

            # deal cards
            c1, c2 = p1.pop(0), p2.pop(0)

            # check if need to recurse
            if len(p1) >= c1 and len(p2) >= c2:
                p1_won, _ = recurse(p1[:c1], p2[:c2])
            else:
                p1_won = c1 > c2

            if p1_won:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)

        return len(p1) > 0, p1 if len(p1) > 0 else p2

    _, p_winner = recurse(player1, player2)
    score = sum([a * b for a, b in zip(p_winner, range(len(p_winner), 0, -1))])
    return score


def main() -> None:
    p1, p2 = parse_input(utils.get_input(__file__))

    # part 1
    winner_score = play_game(p1.copy(), p2.copy())
    print(f"part 1: {winner_score}")

    # part 2
    winner_score = play_game_recursive(p1, p2)
    print(f"part 2: {winner_score}")


if __name__ == "__main__":
    main()
