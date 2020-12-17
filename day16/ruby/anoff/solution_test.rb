require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def test_Rule
    r = Rule.new("asdf", "2-10", "20-33")
    assert_equal true, r.valid?(2)
    assert_equal true, r.valid?(10)
    assert_equal false, r.valid?(11)
    assert_equal true, r.valid?(20)
    assert_equal true, r.valid?(23)
    assert_equal true, r.valid?(33)
    assert_equal false, r.valid?(40)
  end

  def test_RuleSet
    rs = RuleSet.new
    r1 = Rule.new("asdf", "2-10", "20-33")
    r2 = Rule.new("bla", "4-15", "50-64")
    rs.add(r1).add(r2)
    assert_equal true, rs.valid?(2)
    assert_equal true, rs.valid?(14)
    assert_equal false, rs.valid?(19)
    assert_equal true, rs.valid?(64)
    assert_equal 43, rs.validValues.size, "incorrect number of values, might contain duplicates"
  end

  def test_part1
    rules, ticketMine, ticketsNearby = readInput("./input_test.txt")
    assert_equal 71, part1(rules, ticketMine, ticketsNearby)
  end
  
  def test_Tickets
    t = Tickets.new
    t.add("11,12,13")
    t.add("3,9,18")
    t.add("15,1,5")
    assert_equal [12, 9, 1], t.getField(1)
  end

  def test_findFieldNames
    rules, ticketMine, ticketsNearby = readInput("./input_test2.txt")
    rs = RuleSet.new
    for rule in rules
      name, ranges = rule.split(": ")
      range1, range2 = ranges.split(" or ")
      r = Rule.new(name, range1, range2)
      rs.add(r)
    end

    validTickets = Tickets.new
    for ticket in ticketsNearby
      isValid = true
      for value in ticket.split(",")
        if not rs.valid?(value.to_i)
          isValid = false
        end
      end
      if isValid
        validTickets.add(ticket)
      end
    end
    validTickets.add(ticketMine)
    assert_equal ["row", "class", "seat"], findFieldNames(validTickets, rs)
  end
end