from pathlib import Path
from collections import Counter, defaultdict
from functools import reduce
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return list(map(lambda l: int(l), lines))


def sort_adapters(adapters):
    adapters.append(0)
    sorted_adapters = sorted(adapters)
    sorted_adapters.append(max(sorted_adapters)+3)
    return sorted_adapters


def count_jolt_differences(adapters):
    sorted_adapters = sort_adapters(adapters)
    differences = map(
            lambda e: e[1] - sorted_adapters[e[0] - 1],
            enumerate(sorted_adapters[1:], 1))
    
    return Counter(differences)


def calculate_possible_combinations(adapters):
    sorted_adapters = sort_adapters(adapters)
    combinations = defaultdict(int)
   
    combinations[0] = 1

    for i in sorted_adapters[1:]:
        combinations[i] = combinations[i-1] + combinations[i-2] + combinations[i-3]

    return combinations[max(sorted_adapters)]


@app.command()
def part1(input_file: str):
    jolt_differences = count_jolt_differences(read_input_file(input_file))
    print(f"The solution for part 1 is {jolt_differences[1] * jolt_differences[3]}.")


@app.command()
def part2(input_file: str):
    combinations = calculate_possible_combinations(read_input_file(input_file))
    print(f"The solution for part 2 is {combinations}.")


if __name__ == "__main__":
    app()
