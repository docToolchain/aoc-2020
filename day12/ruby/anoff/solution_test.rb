require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_ShipClass
    s = Ship.new
    assert_equal "E", s.heading
    s.move("R90")
    assert_equal "S", s.heading
    s.move("L270")
    assert_equal "W", s.heading
    s.move("R180")
    assert_equal "E", s.heading
    s.move("L360")
    assert_equal "E", s.heading
  end

  def test_part1
    input = readInput("./input_test.txt")
    assert_equal 25, part1(input)
  end

  def test_waypoint
    s = Ship.new
    assert_equal Pos2D.new(10, 1), s.waypoint
    s.move_with_waypoint("L90")
    assert_equal Pos2D.new(-1, 10), s.waypoint
    s.move_with_waypoint("L180")
    assert_equal Pos2D.new(1, -10), s.waypoint
    s.move_with_waypoint("R270")
    assert_equal Pos2D.new(10, 1), s.waypoint
  end
  def test_part2
    input = readInput("./input_test.txt")
    assert_equal 286, part2(input)
  end
end