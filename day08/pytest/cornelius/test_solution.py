from pathlib import Path

#tag::test_star1[]
example_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

def test_example1():
    assert solve1(example_input) == 5

def solve1(input_data):
    terminates, acc = run_code(input_data.splitlines())
    return acc

def run_code(instructions):
    executed = set()
    acc = 0
    pc = 0
    while not pc in executed and pc < len(instructions):
        executed.add(pc)
        cmd = instructions[pc]
        opcode, arg_str = cmd.split()
        arg = int(arg_str)
        if opcode == "nop":
            pc += 1
        elif opcode == "acc":
            acc += arg
            pc += 1
        elif opcode == "jmp":
            pc += arg
    return pc == len(instructions), acc
#end::test_star1[]

#tag::star1[]
def read_input():
    with Path("input.txt").open() as f:
        return f.read()

puzzle_input = read_input()

def test_answer1():
    assert solve1(puzzle_input) == 2003
#end::star1[]

#tag::test_star2[]
def test_example2():
    assert solve2(example_input) == 8

def solve2(input_data):
    instructions = input_data.splitlines()
    for i in range(0,len(instructions)):
        fixed_code = []
        for j, cmd in enumerate(instructions):
            if i == j and "nop" in cmd:
                cmd = cmd.replace("nop", "jmp")
            fixed_code.append(cmd)
        terminates, acc = run_code(fixed_code)
        if terminates:
            return acc

        fixed_code = []
        for j, cmd in enumerate(instructions):
            if i == j and "jmp" in cmd:
                cmd = cmd.replace("jmp", "nop")
            fixed_code.append(cmd)
        terminates, acc = run_code(fixed_code)
        if terminates:
            return acc
    return None
#end::test_star2[]

#tag::star2[]
def test_answer2():
    assert solve2(puzzle_input) == 1984
#end::star2[]
