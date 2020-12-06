from pathlib import Path
from functools import reduce
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return lines


def parse_groups(lines):
    groups = [[]]
    for l in lines:
        if l == "\n":
            groups.append([])
        else:
            groups[-1].append({c for c in l.strip()})
    return groups


def unique_questions_in_groups(groups):
    return list(map(lambda g: set().union(*g), groups))


def common_questions_in_groups(groups):
    return list(map(lambda g: g[0].intersection(*g[1:]), groups))


@app.command()
def part1(input_file: str):
    groups = parse_groups(read_input_file(input_file))
    unique_questions = unique_questions_in_groups(groups)
    sum_of_count = reduce(lambda s, q: s + len(q), unique_questions, 0)

    print(f"The sum of the unique question count is {sum_of_count}")


@app.command()
def part2(input_file: str):
    groups = parse_groups(read_input_file(input_file))
    common_questions = common_questions_in_groups(groups)
    sum_of_count = reduce(lambda s, q: s + len(q), common_questions, 0)

    print(f"The sum of the common question count is {sum_of_count}")


if __name__ == "__main__":
    app()
