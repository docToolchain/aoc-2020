require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_timeUntilDeparture
    assert_equal 5, timeUntilDeparture(59, 939)
  end
  def test_part1
    input = readInput("./input_test.txt")
    assert_equal 295, part1(input)
  end

  def test_part2
    assert_equal 3417, part2("17,x,13,19")
    assert_equal 754018, part2("67,7,59,61")
    assert_equal 779210, part2("67,x,7,59,61")
    assert_equal 1261476, part2("67,7,x,59,61")
    assert_equal 1202161486, part2("1789,37,47,1889")
    assert_equal 1068781, part2("7,13,x,x,59,x,31,19")
  end
end