from pathlib import Path
from functools import reduce
import typer


LETTER_MAP = {"B": "1", "F": "0", "R": "1", "L": "0"}


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    lines = list(map(lambda s: s.strip(), lines))
    return lines


def convert_letter(l):
    return LETTER_MAP[l]


def convert_to_binary(line):
    return reduce(lambda s, l: s + convert_letter(l), line, "")


def convert_to_int(line):
    return int(line, 2)


@app.command()
def part1(input_file: str):
    seat_numbers = read_input_file(input_file)
    seat_numbers = map(lambda l: convert_to_binary(l), seat_numbers)
    seat_numbers = map(lambda l: convert_to_int(l), seat_numbers)
    max_seat_number = max(seat_numbers)

    print(f"The maximum seat number is {max_seat_number}")


@app.command()
def part2(input_file: str):
    seat_numbers = read_input_file(input_file)
    seat_numbers = map(lambda l: convert_to_binary(l), seat_numbers)
    seat_numbers = map(lambda l: convert_to_int(l), seat_numbers)
    seat_numbers = sorted(seat_numbers)

    missing_seats = list(filter(
            lambda s: s+1 in seat_numbers
                      and s-1 in seat_numbers
                      and s not in seat_numbers,
            range(min(seat_numbers)+1, max(seat_numbers))))

    print(f"The missing seat number is {missing_seats[0]}")


if __name__ == "__main__":
    app()
