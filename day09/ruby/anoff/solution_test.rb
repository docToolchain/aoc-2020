require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_validNumber
    r1 = (1..25).to_a
    assert_equal true, validNumber?(r1, 26)
    assert_equal true, validNumber?(r1, 49)
    assert_equal false, validNumber?(r1, 100)
    assert_equal false, validNumber?(r1, 50)

    r2 = ((1..19).to_a + (21..25).to_a).append(45)
    assert_equal true, validNumber?(r2, 26)
    assert_equal false, validNumber?(r2, 65)
    assert_equal true, validNumber?(r2, 64)
    assert_equal true, validNumber?(r2, 66)
  end
  def test_part1
    input = readInput("./input_test.txt")
    assert_equal 127, part1(input, 5)
  end

  def test_findRangeForSum
    input = readInput("./input_test.txt")
    assert_equal [15, 25, 47, 40], findRangeForSum(input, 127)
  end
  def test_part2
    input = readInput("./input_test.txt")
    assert_equal 62, part2(input, 127)
  end
end