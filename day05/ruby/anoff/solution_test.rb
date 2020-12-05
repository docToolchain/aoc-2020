require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_binSpace2RowCol
    d = "FBFBBFFRLR"

    assert_equal [44, 5], binSpace2RowCol(d), "Incorrect result for input"
  end
end