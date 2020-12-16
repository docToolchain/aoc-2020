import pytest



def test_1():
    from util import Schedule
    schedule = Schedule();
    schedule.loadFromFile("testinput.txt")

    depart = schedule.getNextDepartment()

    assert 59 == depart["bus"]
    assert 944 == depart["time"]







  