from pathlib import Path
from functools import reduce
from operator import mul

import typer

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return int(lines[0]), lines[1].strip().split(",")


def parse_second_line(line):
    ids = []
    remainders = []
    for e in enumerate(line):
        if e[1].isdigit():
            i = int(e[1])
            d = int(e[0])

            ids.append(i)
            remainders.append((i - d) % i)
    return ids, remainders


def crt(modulos, remainders):
    solution = 0

    for e in enumerate(modulos):
        i, m = e
        for k in range(1, m+1):
            s = k * reduce(mul, filter(lambda n: n != m, modulos))
            if s % m == remainders[i]:
                solution += s
                break

    product = reduce(mul, modulos)

    while solution >= product:
        solution -= product

    return solution


@app.command()
def part1(input_file: str):
    time, busses = read_input_file(input_file)
    busses = map(lambda i: int(i), filter(lambda s: s.isdigit(), busses))
    wating_time = reduce(lambda a, b: a if a[1] < b[1] else b,
                           map(lambda b: (b, b - time % b), busses))
    print(f"The bus ID is {wating_time[0]} and the waiting time {wating_time[1]}.")
    print(f"Therefor the solution to the puzzle is {wating_time[0] * wating_time[1]}.")


@app.command()
def part2(input_file: str):
    _, line = read_input_file(input_file)
    ids, remainders = parse_second_line(line)
    solution = crt(ids, remainders)

    print(f"The solution for part 2 is {solution}")


if __name__ == "__main__":
    app()
