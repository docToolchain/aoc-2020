from pathlib import Path
from functools import reduce
from collections import defaultdict
import typer

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return list(map(lambda l: l.strip(), lines))


def parse_rules(lines):
    rules = dict()

    for line in lines:
        field, ranges = line.split(": ")
        range1, range2 = ranges.split(" or ")
        low1, high1 = map(lambda v: int(v), range1.split("-"))
        low2, high2 = map(lambda v: int(v), range2.split("-"))
        allowed_values = set(range(low1, high1 + 1)).union(range(low2, high2 + 1))

        rules[field] = allowed_values

    return rules


def parse_input(lines):
    i = lines.index("")
    rules = parse_rules(lines[0:i])
    ticket = list(map(lambda v: int(v), lines[i+2].split(",")))
    other_tickets = list(map(
                             lambda l: list(map(lambda v: int(v), l.split(","))),
                             lines[i+5:]))

    return rules, ticket, other_tickets


def check_value(v, rules):
    return any(map(lambda r: v in r, rules.values()))

def invalid_values(values, rules):
    checked_values = map(lambda v: (v, check_value(v, rules)), values)
    invalid_values = filter(lambda v: v[1] == False, checked_values)
    return list(map(lambda v: v[0], invalid_values))


def check_tickets(tickets, rules):
    return list(map(lambda t: (t, invalid_values(t, rules)), tickets))


def find_rule_positions(tickets, rules):
    position_constraints = defaultdict(list)

    for i in range(len(tickets[0])):
        values = list(map(lambda t: t[i], tickets))

        checked_rules = map(lambda r: (r, invalid_values(values, {r: rules[r]})), rules)
        valid_rules = list(filter(lambda r: r[1] == [], checked_rules))
        for r in valid_rules:
            position_constraints[r[0]].append(i)

    positions = dict()
    while len(positions) < len(tickets[0]):
        r = list(filter(lambda c: len(position_constraints[c]) == 1, position_constraints))
        rule = r[0]
        position = position_constraints[rule][0]
        positions[rule] = position

        for c in position_constraints:
            if position in position_constraints[c]:
                position_constraints[c].remove(position)

    return positions


@app.command()
def part1(input_file: str):
    rules, ticket, other = parse_input(read_input_file(input_file))
    checked_tickets = check_tickets(other, rules)
    error_rate = sum(reduce(lambda l, t: l + t[1], checked_tickets, []))

    print(f"The error rate of the tickets is {error_rate}")


@app.command()
def part2(input_file: str):
    rules, ticket, other = parse_input(read_input_file(input_file))
    checked_tickets = check_tickets(other, rules)

    valid_tickets = filter(lambda t: t[1] == [], checked_tickets)
    valid_tickets = list(map(lambda t: t[0], valid_tickets))

    positions = find_rule_positions(valid_tickets, rules)

    departure_fields = filter(lambda f: "departure" in f, positions)

    result = reduce(lambda p, f: p * ticket[positions[f]], departure_fields, 1)

    print(f"The product of the values is {result}")


if __name__ == "__main__":
    app()
