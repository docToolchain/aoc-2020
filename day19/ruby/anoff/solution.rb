#!/usr/bin/ruby
require_relative "./rule.rb"

def readInput(path)
  rules, messages = File.read(path).split("\n\n")
  return rules.split("\n"), messages.split("\n")
end

def constructRuleSet(rules)
  rs = RuleSet.new
  for rule in rules
    r = Rule.new(rule)
    rs.add(r)
  end
  return rs
end
def part1 (rules, messages)
  rs = constructRuleSet(rules)
  rs.populate
  allowedValues = rs.getRule(0).values
  validMessages = 0
  for m in messages
    if allowedValues.include?(m)
      validMessages += 1
    end
  end
  return validMessages
end

def part1_fast (rules, messages)
  rules = rules.filter{|r| not [0, 8, 11].include?(r.split(":")[0].to_i) }
  rs = constructRuleSet(rules)
  rs.populate
  # 0: 8 11
  # 8: 42
  # 11: 42 31
  validMessages = 0
  for m in messages
    rule42 = "("+rs.getRule(42).values.join("|")+")"
    rule31 = "("+rs.getRule(31).values.join("|")+")"
    if m.match(/^#{rule42}#{rule42}#{rule31}$/)
      validMessages += 1
    end
  end
  return validMessages
end

def part2 (rules, messages)
  rules = rules.filter{|r| not [0, 8, 11].include?(r.split(":")[0].to_i) }
  rs = constructRuleSet(rules)
  rs.populate
  # 0: 8 11
  # 8: 42 | 42 8
  # 11: 42 31 | 42 11 31

  # examples
  # 42 42 31
  # 42 42 42 31
  # 42 42 42 31 31
  # 42 42 31
  validMessages = 0
  for m in messages
    rule42 = "("+rs.getRule(42).values.join("|")+")"
    rule31 = "("+rs.getRule(31).values.join("|")+")"
    # YOLO have to figure out that the part for rule 11 matches equal times 42&31 so just bruteforce it
    for n in 1..8
      if m.match(/^#{rule42}{#{n+1},}#{rule31}{#{n}}$/)
        validMessages += 1
        break
      end
    end
  end
  return validMessages
end

if __FILE__ == $PROGRAM_NAME
  rules, messages = readInput("./input.txt")
  puts "Solution for part1: %d" % part1_fast(rules, messages)
  puts "Solution for part2: #{part2(rules, messages)}" # 292, too low, 382 too high, 281 too low, 365
end
