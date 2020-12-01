from pathlib import Path
import itertools
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    """ read the input file and convert the contents
        to a list of ints """

    p = Path(input_file_path)

    with p.open() as f:
        data = list(map(int, f.readlines()))

    return data


def find_combinations(values, length, function):
    """
    Builds all combinations of length length from the values.
    Filters the resultung list using the supllied function.
    """

    all_combinations = itertools.combinations(values, length)
    return list(filter(function, all_combinations))


@app.command()
def expense_report_1(input_file: str):
    """
    Find the combination of two numbers in the input for which a + b == 2020.
    The function prints the product of these two numbers, i.e. a*b.
    """

    values = read_input_file(input_file)
    a, b = find_combinations(values, 2, lambda e: sum(e) == 2020)[0]
    print(a * b)


@app.command()
def expense_report_2(input_file: str):
    """
    Find the combination of three numbers in the input for which
    a + b + c == 2020.
    The function prints the product of these three numbers, i.e. a*b*c.
    """

    values = read_input_file(input_file)
    a, b, c = find_combinations(values, 3, lambda e: sum(e) == 2020)[0]
    print(a * b * c)


if __name__ == "__main__":
    app()
