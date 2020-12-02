import pytest


def test_count():
    from util import count
    assert 1 == count("abcde",'a')
    assert 0 == count("cdefg",'b')
    assert 9 == count("ccccccccc",'c')

def test_check():
    from util import check
    assert 1 == check("abcde",1,'a') 
    assert 0 == check("abcde",3,'a')
    assert 0 == check("cdefg",1,'b')
    assert 0 == check("cdefg",3,'b')
    assert 1 == check("ccccccccc",2,'c')
    assert 1 == check("ccccccccc",9,'c')