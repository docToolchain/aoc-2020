import pytest



def test_1():
    from util import Cube
    cube = Cube();
    cube.loadFromFile("testinput.txt")

    assert 5 == cube.count()
  
def test_2():
    from util import Cube
    cube = Cube();
    cube.loadFromFile("testinput.txt")

    for i in range(0,6):
        cube = cube.next()
    
    assert 112 == cube.count()

def test_3():
    from util import Cube4D
    cube = Cube4D();
    cube.loadFromFile("testinput.txt")

    assert 5 == cube.count()

def test_4():
    from util import Cube4D
    cube = Cube4D();
    cube.loadFromFile("testinput.txt")

    for i in range(0,6):
        cube = cube.next()
    
    assert 848 == cube.count()