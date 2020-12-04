import pytest


class TreeMapMock():

    def __init__(self):
        """Read file to map"""
        self._rows = []
    
    def append(self,row):
        return self._rows.append(row)

    @property
    def width(self):
        return len(self._rows[0])

    @property
    def height(self):
        return len(self._rows)

    def get(self,x,y):
        return self._rows[y][x]

def test_count():
    from util import count_trees
    map = TreeMapMock();

    map.append("..##.......");
    map.append("#...#...#..");
    map.append(".#....#..#.");
    map.append("..#.#...#.#");
    map.append(".#...##..#.");
    map.append("..#.##.....");
    map.append(".#.#.#....#");
    map.append(".#........#");
    map.append("#.##...#...");
    map.append("#...##....#");
    map.append(".#..#...#.#");
    
    assert 2 == count_trees(map,1,1)
    assert 7 == count_trees(map,3,1)
    assert 3 == count_trees(map,5,1)
    assert 4 == count_trees(map,7,1)
    assert 2 == count_trees(map,1,2)

