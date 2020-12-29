require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_part1
    rules, messages = readInput("./input_test.txt")
    assert_equal 2, part1(rules, messages)
  end
  def test_part1_fast
    rules, messages = readInput("./input_test2.txt")
    assert_equal 3, part1(rules, messages)
    assert_equal 3, part1_fast(rules, messages)
  end
  def test_RuleSet
    rules, messages = readInput("./input_test.txt")
    rs = constructRuleSet(rules)
    rs.populate
    assert_equal ["aa", "bb"], rs.getRule(2).values
    assert_equal ["ab", "ba"], rs.getRule(3).values
    assert_equal ["aaab", "aaba", "bbab", "bbba", "abaa", "abbb", "baaa", "babb"], rs.getRule(1).values
    assert_equal ["aaaabb", "aaabab", "abbabb", "abbbab", "aabaab", "aabbbb", "abaaab", "ababbb"], rs.getRule(0).values
  end
  def test_part2
    rules, messages = readInput("./input_test2.txt")
    assert_equal 3, part1(rules, messages)
    assert_equal 12, part2(rules, messages)
  end
end