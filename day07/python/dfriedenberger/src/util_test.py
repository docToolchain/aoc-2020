import pytest



def test_1():
    from util import read_file_to_list
    from util import hasShinyGold
    result = 0
    data = read_file_to_list("testinput.txt")
    for key in data:
        if key == "shiny gold":
            continue #Ignore
        if hasShinyGold(data,key):
            result = result + 1
    assert 4 == result

def test_2():
    from util import read_file_to_list
    from util import countBags
    
    data = read_file_to_list("testinput.txt")
    result = countBags(data,"shiny gold") - 1
    assert 32 == result

def test_2():
    from util import read_file_to_list
    from util import countBags
    
    data = read_file_to_list("testinput2.txt")
    result = countBags(data,"shiny gold") - 1
    assert 126 == result
