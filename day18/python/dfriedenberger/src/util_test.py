import pytest



  
def test_solve():
    from util import solve
   
    assert 26 == solve("2 * 3 + (4 * 5)")
    assert 437 == solve("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    assert 12240 == solve("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    assert 13632 == solve("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")

def test_solve2():
    from util import solve2
   
    assert 51 == solve2("1 + (2 * 3) + (4 * (5 + 6))")
    assert 46 == solve2("2 * 3 + (4 * 5)")
    assert 1440 == solve2("8 * 3 + 9 + 3 * 4 * 3")
    assert 1445 == solve2("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    assert 669060 == solve2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    assert 23340 == solve2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")

