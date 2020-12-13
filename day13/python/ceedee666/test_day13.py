from day13 import crt, parse_second_line


def test_crt():
    ids, remainders = parse_second_line(["17", "x", "13", "19"])
    assert 3417 == crt(ids, remainders)

    ids, remainders = parse_second_line(["67", "7", "59", "61"])
    assert 754018 == crt(ids, remainders)

    ids, remainders = parse_second_line(["67", "7", "x", "59", "61"])
    assert 1261476 == crt(ids, remainders)
