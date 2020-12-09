import pytest



def test_1():
    from util import read_file_to_list
    from util import NumberCache
    data = read_file_to_list("testinput.txt")
    preamble = 5
    nc = NumberCache(preamble)

 
    for i in range(len(data)):

        if i >= preamble:
            if not nc.valid(data[i]):
                ivn = data[i]
        nc.add(data[i])
    assert ivn == 127

