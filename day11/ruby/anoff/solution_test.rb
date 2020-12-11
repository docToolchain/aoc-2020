require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_SeatmapClass
    input = readInput("./input_test.txt")
    s = Seatmap.new(input)
    assert_equal 0, s.occupiedSeatCount(0, 0)
    s.setOccupied(3, 2, true)
    assert_equal 1, s.occupiedSeatCount(2, 2)
    s.setOccupied(3, 3, true)
    assert_equal 2, s.occupiedSeatCount(2, 2)
  end

  # visual testing.. :D
  def Ttest_SeatmapStep
    input = readInput("./input_test.txt")
    s = Seatmap2.new(input)
    s.print
    s.step
    puts s.occupiedSeatCount(2, 0)
  end

  def test_part1
    input = readInput("./input_test.txt")
    assert_equal 37, part1(input)
  end

  def test_part2
    input = readInput("./input_test.txt")
    assert_equal 26, part2(input)
  end
end