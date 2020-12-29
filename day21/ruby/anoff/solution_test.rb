require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_part1
    list = readInput("./input_test.txt")
    assert_equal 5, part1(list)
  end
end