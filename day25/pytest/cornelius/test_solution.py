from pathlib import Path

#tag::loop_size[]
def test_find_loop_size():
    assert find_loop_size(5764801) == 8
    assert find_loop_size(17807724) == 11

def find_loop_size(public_key):
    result = 1
    count = 0
    subject_number = 7
    while result != public_key:
        result *= subject_number
        result = result % 20201227
        count += 1
    return count
#end::loop_size[]

#tag::transform[]
def test_transform():
    assert transform(17807724, 8) == 14897079
    assert transform(5764801, 11) == 14897079

def transform(subject_number, loop_size):
    result = 1
    for i in range(loop_size):
        result *= subject_number
        result = result % 20201227
    return result
#end::transform[]

#tag::star1[]
def solve1():
    public_key_card = 10943862
    public_key_door = 12721030
    loop_size_card = find_loop_size(public_key_card)
    return transform(public_key_door, loop_size_card)

def test_answer1():
    assert solve1() == 5025281
#end::star1[]
