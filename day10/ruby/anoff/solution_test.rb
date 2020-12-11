require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_joltageDiff
    a1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    assert_equal [7, 0, 5], joltageDiff(a1)
    a2 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
    assert_equal [22, 0, 10], joltageDiff(a2  )
  end
  def test_part1
    input = readInput("./input_test.txt")
  end
end