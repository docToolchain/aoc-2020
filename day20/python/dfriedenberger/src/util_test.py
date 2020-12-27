import pytest



def test_count():
    from util import read_file_to_list
    from util import find_solution
    from util import find_pattern
    from util import concat_Tiles
    
    tiles = read_file_to_list("testinput.txt")

    #optimazation, create variants once
    for tile in tiles:
        tile.createVariants()

    solution = find_solution(tiles,[],set(),0,0)

    assert 20899048083289 == solution[0][0].id * solution[0][-1].id * solution[-1][0].id * solution[-1][-1].id

    monster = []
    monster.append("                  # ")
    monster.append("#    ##    ##    ###")
    monster.append(" #  #  #  #  #  #   ")

    map = concat_Tiles(solution)
    map.createVariants()

    for m in map.getVariants():
        r = find_pattern(m,monster)
        if len(r) == 0: continue
        assert 273 == m.count() - len(r) * 15


