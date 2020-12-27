import pytest



def test_count():
    from util import read_file_to_list
    from util import flip_tiles
    from util import daily_flip_tiles
    from util import Tiles
    lines = read_file_to_list("testinput.txt")
    tiles = Tiles()
    for line in lines:
        flip_tiles(tiles,line)
    c = tiles.countBlack()
    assert 10 == c

    daily_flip_tiles(tiles)
    c = tiles.countBlack()
    assert 15 == c
