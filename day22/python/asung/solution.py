#!/usr/bin/env python3
import os
from typing import List, Set, Tuple
import numpy as np


class Solver:
    def __init__(self, filepath: str) -> None:
        with open(filepath, 'r') as text_file:
            groups = list(map(lambda data: data.split('\n'), text_file.read().strip().split('\n\n')))
        self.cards1 = list(map(int, groups[0][1:]))
        self.cards2 = list(map(int, groups[-1][1:]))
        self.game_count = 0
        # Note: Debug mode prints interim results for part 2, as seen in the original examples of the puzzle.
        # Use at your own risk! The number of games played for your puzzle input will be very high. It's over 9000!
        self.debug_part2 = False

    @staticmethod
    def calculate_score(cards: List[int]) -> int:
        return sum(np.multiply(cards, range(len(cards), 0, -1)))

    def debug(self, *values: object) -> None:
        """Print values in debug mode only."""
        if self.debug_part2:
            print(*values)

    def play_recursive_combat(self, game: int, cards1: List[int], cards2: List[int]) -> Tuple[int, List[int], List[int]]:
        """Play a game of recursive combat, and return (winner, cards of player 1, cards of player 2)."""
        self.game_count = game
        configurations = set()  # type: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]]
        game_round = 0
        self.debug(f"=== Game {game} ===\n")
        while cards1 and cards2:
            configuration = (tuple(cards1), tuple(cards2))
            # Check for repeated configuration.
            if configuration in configurations:
                # Win by infinite game prevention rule.
                self.debug(f"The winner of game {game} is player 1 due to the infinite game prevention rule!\n")
                return 1, cards1, cards2

            configurations.add(configuration)
            if game_round > 0:
                self.debug()
            game_round += 1
            self.debug(f"-- Round {game_round} (Game {game}) --")
            self.debug(f"Player 1's deck: {', '.join(str(card) for card in cards1)}")
            self.debug(f"Player 2's deck: {', '.join(str(card) for card in cards2)}")
            # Draw cards.
            card1, card2 = cards1.pop(0), cards2.pop(0)
            self.debug(f"Player 1 plays: {card1}")
            self.debug(f"Player 1 plays: {card2}")
            # Check if a recursion is to be played.
            if len(cards1) >= card1 and len(cards2) >= card2:
                self.debug("Playing a sub-game to determine the winner...\n")
                winner, _, _ = self.play_recursive_combat(self.game_count + 1, cards1[:card1], cards2[:card2])
                self.debug(f"...anyway, back to game {game}.")
            else:
                winner = 1 if card1 > card2 else 2
            # Assign cards to winner.
            if winner == 1:
                cards1.extend([card1, card2])
            else:
                cards2.extend([card2, card1])
            self.debug(f"Player {winner} wins round {game_round} of game {game}!")
        # Win by regular combat.
        winner = 1 if cards1 else 2
        self.debug(f"The winner of game {game} is player {winner}!\n")
        return winner, cards1, cards2

    def solve_part1(self) -> int:
        cards1, cards2 = list(self.cards1), list(self.cards2)
        while cards1 and cards2:
            card1, card2 = cards1.pop(0), cards2.pop(0)
            if card1 > card2:
                cards1.extend([card1, card2])
            else:
                cards2.extend([card2, card1])
        winner_cards = cards1 if cards1 else cards2
        return self.calculate_score(winner_cards)

    def solve_part2(self) -> int:
        winner, cards1, cards2 = self.play_recursive_combat(1, list(self.cards1), list(self.cards2))
        winner_cards = cards1 if winner == 1 else cards2
        print("\n== Post-game results ==")
        print(f"Player 1's deck: {', '.join(str(card) for card in cards1)}")
        print(f"Player 2's deck: {', '.join(str(card) for card in cards2)}")
        print()
        print(f"{self.game_count} games played.")
        return self.calculate_score(winner_cards)


if __name__ == "__main__":
    solver = Solver(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
