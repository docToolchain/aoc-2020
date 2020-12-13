import day11

def prepare_data():
    s0 = ["L.LL.LL.LL",
          "LLLLLLL.LL",
          "L.L.L..L..",
          "LLLL.LL.LL",
          "L.LL.LL.LL",
          "L.LLLLL.LL",
          "..L.L.....",
          "LLLLLLLLLL",
          "L.LLLLLL.L",
          "L.LLLLL.LL"]

    s1 = ["#.##.##.##",
          "#######.##",
          "#.#.#..#..",
          "####.##.##",
          "#.##.##.##",
          "#.#####.##",
          "..#.#.....",
          "##########",
          "#.######.#",
          "#.#####.##"]

    s2 = ["#.LL.L#.##",
          "#LLLLLL.L#",
          "L.L.L..L..",
          "#LLL.LL.L#",
          "#.LL.LL.LL",
          "#.LLLL#.##",
          "..L.L.....",
          "#LLLLLLLL#",
          "#.LLLLLL.L",
          "#.#LLLL.##"]

    result = []

    result.append(list(map(lambda l: list(l), s0)))
    result.append(list(map(lambda l: list(l), s1)))
    result.append(list(map(lambda l: list(l), s2)))

    return result


def test_simulate_step():
    test_data = prepare_data()
    assert test_data[1] == day11.simulate_step(test_data[0])
    assert test_data[2] == day11.simulate_step(test_data[1])


def test_simulate():
    test_data = prepare_data()
    simulator = day11.simulator(test_data[0])
    assert test_data[1] == next(simulator)
    assert test_data[2] == next(simulator)


def prepare_data_part_2():
    s0 = ["#.##.##.##",
          "#######.##",
          "#.#.#..#..",
          "####.##.##",
          "#.##.##.##",
          "#.#####.##",
          "..#.#.....",
          "##########",
          "#.######.#",
          "#.#####.##"]

    s1 = ["#.LL.LL.L#",
          "#LLLLLL.LL",
          "L.L.L..L..",
          "LLLL.LL.LL",
          "L.LL.LL.LL",
          "L.LLLLL.LL",
          "..L.L.....",
          "LLLLLLLLL#",
          "#.LLLLLL.L",
          "#.LLLLL.L#"]

    s2 = ["#.L#.##.L#",
          "#L#####.LL",
          "L.#.#..#..",
          "##L#.##.##",
          "#.##.#L.##",
          "#.#####.#L",
          "..#.#.....",
          "LLL####LL#",
          "#.L#####.L",
          "#.L####.L#"]

    s3 = ["#.L#.L#.L#",
          "#LLLLLL.LL",
          "L.L.L..#..",
          "##LL.LL.L#",
          "L.LL.LL.L#",
          "#.LLLLL.LL",
          "..L.L.....",
          "LLLLLLLLL#",
          "#.LLLLL#.L",
          "#.L#LL#.L#"]

    result = []

    result.append(list(map(lambda l: list(l), s0)))
    result.append(list(map(lambda l: list(l), s1)))
    result.append(list(map(lambda l: list(l), s2)))
    result.append(list(map(lambda l: list(l), s3)))

    return result


def test_simulate_step_part2():
    test_data = prepare_data_part_2()
    assert test_data[1] == day11.simulate_step(test_data[0], 5, 1)
    assert test_data[2] == day11.simulate_step(test_data[1], 5, 1)
    assert test_data[3] == day11.simulate_step(test_data[2], 5, 1)


