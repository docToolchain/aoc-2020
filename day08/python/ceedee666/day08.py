from pathlib import Path
from collections import defaultdict
from copy import deepcopy

import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return lines


def parse_input(lines):
    return list(map(
        lambda l: defaultdict(int, {"operation": l[:3], "value": int(l[4:])}),
        lines))


def run_instructions(instructions):
    accumulator = 0
    instruction_pointer = 0
    infinite_loop = False

    while instruction_pointer < len(instructions) \
            and not infinite_loop:
        
        if instructions[instruction_pointer]["execution_count"] == 0:

            instructions[instruction_pointer]["execution_count"] += 1
            operation = instructions[instruction_pointer]["operation"]

            if operation == "nop":
                instruction_pointer += 1
            elif operation == "jmp":
                instruction_pointer += instructions[instruction_pointer]["value"]
            elif operation == "acc":
                accumulator += instructions[instruction_pointer]["value"]
                instruction_pointer += 1
        
        else:
            infinite_loop = True
            
    return accumulator, infinite_loop


def build_program_variants(instructions):
    variants = []

    for i in range(len(instructions)):
        if instructions[i]["operation"] in ["jmp", "nop"]:
            variant = deepcopy(instructions)
            if variant[i]["operation"] == "jmp":
                variant[i]["operation"] = "nop"
            else:
                variant[i]["operation"] = "jmp"
            variants.append(variant)

    return variants


@app.command()
def part1(input_file: str):
    accumulator, _ = run_instructions(parse_input(read_input_file(input_file)))
    print(f"The value of the accumulator is {accumulator}")


@app.command()
def part2(input_file: str):
    program = parse_input(read_input_file(input_file))
    variants = build_program_variants(program)

    results = map(lambda v: run_instructions(v), variants)
    [result] = list(filter(lambda r: not r[1], results))

    print(f"The value of the accumulator after the program terminates is {result[0]}")


if __name__ == "__main__":
    app()
