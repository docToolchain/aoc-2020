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

end