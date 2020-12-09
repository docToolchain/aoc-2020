require "test/unit"
require_relative './solution'
require_relative './computer'

class TestSolution < Test::Unit::TestCase
  def test_part1
    rules = readInput("./input_test.txt")
    assert_equal 5, part1(rules)
  end
end