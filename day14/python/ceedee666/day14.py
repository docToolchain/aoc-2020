from pathlib import Path
from functools import reduce
from operator import add

import typer

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    program = []

    for line in lines:
        op, val = line.strip().split(" = ")
        if op == "mask":
            program.append({"op": "mask", "val": val})
        else:
            program.append({"op": "mem",
                            "add": int(op[4:-1]),
                            "val": int(val)})
    return program


def apply_bin_mask(mask, val):
    bin_val = f"{bin(val)[2:]:0>36}"
    bin_result = ""

    for i, c in enumerate(mask):
        if c in "01":
            bin_result += c
        else:
            bin_result += bin_val[i]

    return int(bin_result, 2)


def apply_bin_mask_v2(mask, val):
    bin_val = f"{bin(val)[2:]:0>36}"
    values = [""]

    for i, c in enumerate(mask):
        new_values = []
        for v in values:
            if c == "0":
                new_values.append(v + bin_val[i])
            elif c == "1":
                new_values.append(v + c)
            else:
                new_values.append(v + "0")
                new_values.append(v + "1")

        values = new_values

    return list(map(lambda v: int(v, 2), values))


def execute_instruction(memory, instruction, version):
    if instruction["op"] == "mask":
        memory["mask"] = instruction["val"]
    else:
        if version == 1:
            val = apply_bin_mask(memory["mask"], instruction["val"])
            memory[instruction["add"]] = val
        if version == 2:
            addresses = apply_bin_mask_v2(memory["mask"], instruction["add"])
            for address in addresses:
                memory[address] = instruction["val"]

    return memory


def execute_initialization(program, version=1):
    memory = reduce(lambda m, e: execute_instruction(m, e, version), program, dict())
    memory.pop("mask")
    return sum(memory.values())


@app.command()
def part1(input_file: str):
    program = read_input_file(input_file)
    result = execute_initialization(program)
    print(f"The sum of all values in memory is {result}.")


@app.command()
def part2(input_file: str):
    program = read_input_file(input_file)
    result = execute_initialization(program, version=2)
    print(f"The sum of all values in memory is {result}.")


if __name__ == "__main__":
    app()
