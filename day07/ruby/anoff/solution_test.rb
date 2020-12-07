require "test/unit"
require_relative './solution'
require_relative './ruleset'

class TestSolution < Test::Unit::TestCase
  def test_BagClass
    input = ["vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
    "faded blue bags contain no other bags.",
    "dotted black bags contain no other bags."]
    r = Ruleset.new(input)

    b = r.getBag("vibrant plum")

    assert_equal false, b.expanded?
    b.expandRules(r)
    assert_equal true, b.expanded?
    assert_equal 2, b.contents.size
  end

  def test_part1
    rules = readInput("./input_test.txt")
    assert_equal 4, part1(rules)
  end

  def test_RulesetClass
    input = ["vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
      "faded blue bags contain no other bags.",
      "dotted black bags contain no other bags."]
    r = Ruleset.new(input)

    assert_equal 3, r.bags.size
    assert_equal "faded blue", r.bags[1].color
    assert_equal 2, r.getBag("vibrant plum").rules.size
    assert_equal ["5 faded blue", "6 dotted black"], r.getBag("vibrant plum").rules
  end

  def test_part2
    rules = readInput("./input_test.txt")
    assert_equal 32, part2(rules)

    rules = readInput("./input_test2.txt")
    assert_equal 126, part2(rules)
  end

end