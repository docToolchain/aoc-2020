import pytest


def test_play10():
    from util import play
    init = [3,8,9,1,2,5,4,6,7]
    l = len(init)

    cups = dict()
    for i in range(l):
        cups[init[i]] = init[(i+1) % l]

    play(cups,init[0],10)

    n = 1
    s = ""
    for _ in range(l-1):
        s += str(cups[n])
        n = cups[n]

    assert "92658374" == s

def test_play100():
    from util import play
    init = [3,8,9,1,2,5,4,6,7]
    l = len(init)

    cups = dict()
    for i in range(l):
        cups[init[i]] = init[(i+1) % l]

    play(cups,init[0],100)

    n = 1
    s = ""
    for _ in range(l-1):
        s += str(cups[n])
        n = cups[n]

    assert "67384529" == s