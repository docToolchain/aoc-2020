import pytest



  
def test_process():
    from util import process
    assert 0 == process([0,3,6],10)
    assert 1 == process([1,3,2],2020)

#def test_process2():
#    from util import process
#    assert 175594 == process([1,3,2],30000000)
  