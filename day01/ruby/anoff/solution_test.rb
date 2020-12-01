require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_p1
    d = [
      1721,
      979,
      366,
      299,
      675,
      1456
    ]
    assert_equal 514579, part1(d), "Incorrect result for input"
  end

  def test_p2
    d = [
      1721,
      979,
      366,
      299,
      675,
      1456
    ]
    assert_equal 241861950, part2(d), "Incorrect result for input"
  end
end