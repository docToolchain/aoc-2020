require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_maskedValue
    assert_equal 73, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 11)
    assert_equal 101, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 101)
    assert_equal 64, maskedValue("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 0)
  end
  
  def test_addressModifier
    assert_equal [26, 27, 58, 59], addressModifier("000000000000000000000000000000X1001X", 42)
    assert_equal [16, 17, 18, 19, 24, 25, 26, 27], addressModifier("00000000000000000000000000000000X0XX", 26)
  end
  def test_part2
    input = readInput("./input_test.txt")
    assert_equal 208, part2(input)
  end
end