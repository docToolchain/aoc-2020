import pytest



def test_play():
    from util import play
    from util import read_file_to_list
    from util import count
    p1 , p2  = read_file_to_list("testinput.txt")
    p = play(p1,p2)
    assert 306 == count(p)

def test_play_recursive():
    from util import play_recursive
    from util import read_file_to_list
    from util import count
    p1 , p2  = read_file_to_list("testinput.txt")
    p , _ = play_recursive(p1,p2,0)
    assert 291 == count(p)

def test_endless_loop():
    from util import play
    from util import count
    p = play([ 43, 19 ], [2 , 29 , 14 ])
    assert 0 == count(p)
