require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_part1
    assert_equal 436, part1([0, 3, 6])
    assert_equal 1, part1([1, 3, 2])
    assert_equal 1836, part1([3, 1, 2])
    assert_equal 78, part1([2, 3, 1])
  end
end