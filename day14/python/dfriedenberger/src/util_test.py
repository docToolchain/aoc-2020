import pytest



  
def test_process():
    from util import process
    
    assert 73 == process('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',11)
  
def test_process_address():
    from util import process_address
    l = process_address('000000000000000000000000000000X1001X',42)
    assert 4 == len(l)
    assert 26 == l[0]
    assert 58 == l[1]
    assert 27 == l[2]
    assert 59 == l[3]