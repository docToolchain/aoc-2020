import pytest



def test_1():
    from util import SeatMap
    map = SeatMap();
    map.loadFromFile("testinput.txt")

    cnt = 0
    run = True
    while run:
        seatMapNext = map.next()
        cnt += 1
        if seatMapNext.equals(map): run = False
        map = seatMapNext
        if cnt > 10: break
    
    assert 6 == cnt
    assert 37 == map.count()
  

def test_2():
    from util import SeatMap
    map = SeatMap();
    map.loadFromFile("testinput.txt")

    cnt = 0
    run = True
    while run:
        seatMapNext = map.next2()
        cnt += 1
        if seatMapNext.equals(map): run = False
        map = seatMapNext
        if cnt > 10: break
    
    assert 7 == cnt
    assert 26 == map.count()
  