import pytest



def test_1():
    from util import read_file_to_list
    from util import process
    data = read_file_to_list("testinput.txt")
    terminate, acc = process(data)
    assert terminate == False
    assert acc == 5

def test_2():
    from util import read_file_to_list
    from util import process
    from util import fix_command
    data = read_file_to_list("testinput.txt")
    data1 = fix_command(data,7)
    terminate, acc = process(data1)
    assert terminate == True
    assert acc == 8






