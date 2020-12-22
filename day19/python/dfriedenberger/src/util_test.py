import pytest



  
def test_process():
    from util import read_file_to_list
    from util import match
    rules, rows = read_file_to_list("testinput.txt")

    assert 6 == len(rules)
    assert 5 == len(rows)
    
    assert True  == match(rules,rows[0])
    assert False == match(rules,rows[1])
    assert True  == match(rules,rows[2])
    assert False == match(rules,rows[3])
    assert False == match(rules,rows[4])


def test_process():
    from util import read_file_to_list
    from util import match
    rules, rows = read_file_to_list("testinput2.txt")

    valid = 0
    for row in rows:
        if match(rules,row):
            valid += 1
    assert valid  == len(rows)


