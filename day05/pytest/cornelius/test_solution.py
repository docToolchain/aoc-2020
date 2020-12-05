from pathlib import Path

#tag::read_input[]
def read_input(day):
    with Path("input.txt").open() as f:
        return f.read()

puzzle_input = read_input(5)
#end::read_input[]

#tag::decode_boarding_pass[]
def decode_boarding_pass(code):
    binary_row = code[0:7].replace("F", "0").replace("B", "1")
    binary_column = code[7:10].replace("R", "1").replace("L", "0")
    row = int(binary_row, 2)
    column = int(binary_column, 2)
    seat_id = row * 8 + column
    return row, column, seat_id

def test_decode_boarding_pass():
    assert decode_boarding_pass("FBFBBFFRLR") == (44, 5, 357)
    assert decode_boarding_pass("BFFFBBFRRR") == (70, 7, 567)
    assert decode_boarding_pass("FFFBBBFRRR") == (14, 7, 119)
    assert decode_boarding_pass("BBFFBBFRLL") == (102, 4, 820)
#end::decode_boarding_pass[]

#tag::star1[]
def solve1(input):
    max_id = 0
    for line in input.splitlines():
        if line:
            row, column, seat_id = decode_boarding_pass(line)
            if seat_id > max_id:
                max_id = seat_id
    return max_id

def test_answer1():
    assert solve1(puzzle_input) == 928
#end::star1[]

#tag::star2[]
def solve2(input):
    seats = {}
    for line in input.splitlines():
        if line:
            row, column, seat_id = decode_boarding_pass(line)
            seats[seat_id] = (row, column)
    for i in range(0,1023):
        if i+1 in seats and i-1 in seats and not i in seats:
            return i
    return 0

def test_answer2():
    assert solve2(puzzle_input) == 610
#end::star2[]
