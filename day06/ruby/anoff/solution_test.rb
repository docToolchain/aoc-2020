require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_parseGroups
    input = readInput("./input_test.txt")

    assert_equal 5, parseGroups(input).size, "Incorrect result for input"
  end

  def test_mergeGroupAnswers
    input = ["aabbacc"]

    assert_equal ["abc"], mergeGroupAnswers(input), "Incorrect result for input"
  end

  def test_part2
    input = readInput("./input_test.txt")

    assert_equal 6, part2(input), "Incorrect result for input"
  end
end