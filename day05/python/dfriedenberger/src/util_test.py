import pytest



def test_get_int():
    from util import get_int
    assert 567 == get_int("BFFFBBFRRR")
    assert 119 == get_int("FFFBBBFRRR")
    assert 820 == get_int("BBFFBBFRLL")