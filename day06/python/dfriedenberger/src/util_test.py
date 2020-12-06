import pytest



def test_1():
    from util import toSet
    assert {'a' , 'b'} == toSet([{'a' , 'b'},{'a'}]);

def test_2():
    from util import toSet2
    assert {'a'} == toSet2([{'a' , 'b'},{'a'}]);
