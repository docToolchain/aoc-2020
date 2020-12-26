import pytest


def test_insert1():
    from util import insert
    a = [1,2,3,4,5]
    insert(a,[6,7,8],1)
    assert a == [1,6,7,8,2,3,4,5]

def test_insert2():
    from util import insert
    a = [1,2,3,4,5]
    insert(a,[6,7,8],5)
    assert a == [1,2,3,4,5,6,7,8]


def test_play1():
    from util import play
    a = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    play(a)
    assert a == [2, 8, 9, 1, 5, 4, 6, 7, 3]


def test_play2():
    from util import play
    a = [2, 8, 9, 1, 5, 4, 6, 7, 3]
    play(a)
    assert a == [ 5, 4, 6, 7, 8, 9, 1, 3 , 2]

def test_play3():
    from util import play
    a = [5, 4, 6, 7, 8, 9, 1, 3 , 2]
    play(a)
    assert a == [ 8, 9, 1, 3, 4, 6, 7, 2, 5]

