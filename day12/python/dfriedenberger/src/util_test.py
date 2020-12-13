import pytest



def test_1():
    from util import Ship
    ship = Ship();
  
    ship.process({ "type" : "F", "value" : 10});
    ship.process({ "type" : "N", "value" : 3});
    ship.process({ "type" : "F", "value" : 7});
    ship.process({ "type" : "R", "value" : 90});
    ship.process({ "type" : "F", "value" : 11});

    
    assert 17 == ship.x
    assert -8 == ship.y
    assert 25 == ship.manhattan()
  
def test_rotate():
    from util import Ship
    ship = Ship();

    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    assert 1 == ship.mx
    assert 0 == ship.my
  
    ship.process({ "type" : "L", "value" : 180});
    assert -1 == ship.mx
    assert 0 == ship.my

    ship.process({ "type" : "R", "value" : 90});
    assert 0 == ship.mx
    assert 1 == ship.my

    ship.process({ "type" : "L", "value" : 270});
    assert 1 == ship.mx
    assert 0 == ship.my



def test_rotateV2():
    from util import ShipV2
    ship = ShipV2();

    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    ship.process({ "type" : "L", "value" : 90});
    assert 10 == ship.w[0]
    assert 1 == ship.w[1]
  
    ship.process({ "type" : "R", "value" : 360});
    assert 10 == ship.w[0]
    assert 1 == ship.w[1]

def test_MoveV2():
    from util import ShipV2
    ship = ShipV2();

    ship.process({ "type" : "N", "value" : 2});
    assert 10 == ship.w[0]
    assert 3 == ship.w[1]

    ship.process({ "type" : "S", "value" : 2});
    assert 10 == ship.w[0]
    assert 1 == ship.w[1]

    ship.process({ "type" : "E", "value" : 2});
    assert 12 == ship.w[0]
    assert 1 == ship.w[1]

    ship.process({ "type" : "W", "value" : 2});
    assert 10 == ship.w[0]
    assert 1 == ship.w[1]

def test_ForwardV2():
    from util import ShipV2
    ship = ShipV2();

    ship.process({ "type" : "F", "value" : 2});
    assert 20 == ship.p[0]
    assert 2 == ship.p[1]


def test_V2():
    from util import ShipV2
    ship = ShipV2();
  
    ship.process({ "type" : "F", "value" : 10});
    ship.process({ "type" : "N", "value" : 3});
    ship.process({ "type" : "F", "value" : 7});
    ship.process({ "type" : "R", "value" : 90});
    ship.process({ "type" : "F", "value" : 11});

    assert 214 == ship.p[0]
    assert -72 == ship.p[1]
    assert 286 == ship.manhattan()