from pathlib import Path
from collections import deque
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return [l.strip().replace(" ", "") for l in lines]


def to_rpn(expression, precedence):
    result = ""
    stack = deque()

    for c in expression:
        if c.isnumeric():
            result += c
        else:
            if c in "+-*/":
                while stack and stack[-1] != '(' and precedence[c] <= precedence[stack[-1]]:
                    result += stack.pop()
                stack.append(c)

            elif c == "(":
                stack.append(c)
            elif c == ")":
                current = stack.pop()
                while stack and current != "(":
                    result += current
                    current = stack.pop()

    while stack:
        result += stack.pop()

    return result


def eval_rpn(expression):
    stack = deque()

    for c in expression:
        if c in "+-*/":
            r = stack.pop()
            l = stack.pop()
            r = eval(f"{l}{c}{r}")
            stack.append(r)
        else:
            stack.append(c)

    return int(stack.pop())


@app.command()
def part1(input_file: str):
    expressions = read_input_file(input_file)
    precedence = {"+": 0, "-": 0, "*": 0, "/": 0}
    result = sum(map(lambda e: eval_rpn(to_rpn(e, precedence)), expressions))
    print(f"The sum of the resulting values is {result}")


@app.command()
def part2(input_file: str):
    expressions = read_input_file(input_file)
    precedence = {"+": 1, "-": 0, "*": 0, "/": 0}
    result = sum(map(lambda e: eval_rpn(to_rpn(e, precedence)), expressions))
    print(f"The sum of the resulting values is {result}")



if __name__ == "__main__":
    app()
