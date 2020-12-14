require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_maskedValue
    assert_equal 73, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 11)
    assert_equal 101, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 101)
    assert_equal 64, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 0)
  end
  def test_part1
    #input = readInput("./input_test.txt")
    #assert_equal 295, part1(input)
  end
end