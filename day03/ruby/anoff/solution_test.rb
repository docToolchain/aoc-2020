require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def bluptest_step
    m = readInput("./input_test.txt")

    assert_equal 0, step(m, [0, 0], [3, 1]), "Incorrect result for input"
    assert_equal 1, step(m, [0, 0], [4, 1]), "Incorrect result for input"
  end

  def test_route
    m = readInput("./input_test.txt")

    assert_equal 7, route(m, [0, 0], [3, 1]), "Incorrect result for input"
    assert_equal 2, route(m, [0, 0], [1, 1]), "Incorrect result for input"
  end
end