from day09 import is_number_valid, all_sublists

test_input = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150,
                182, 127, 219, 299, 277, 309, 576]

def test_is_number_valid():
    assert True == is_number_valid([35, 20, 15, 25, 47], 40)
    assert False == is_number_valid([35, 20, 15, 25, 47], 41)


def test_all_sublists():
    test_list = [1, 2, 3, 4]
    sublists = [[1, 2], [1, 2, 3], [1, 2, 3, 4], [2, 3], [2, 3, 4], [3, 4]]
    assert all(map(lambda l: l in sublists, all_sublists(test_list)))
