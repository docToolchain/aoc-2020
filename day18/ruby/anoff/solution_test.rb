require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_calc
    assert_equal 71, calc("1 + 2 * 3 + 4 * 5 + 6")
    assert_equal 26, calc("2 * 3 + (4 * 5)")
    assert_equal 437, calc("5 + (8 * 3 + 9 + 3 * 4 * 3)")
    assert_equal 12240, calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    assert_equal 13632, calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
  end
end