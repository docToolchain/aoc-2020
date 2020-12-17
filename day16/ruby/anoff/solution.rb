#!/usr/bin/ruby
require_relative "./rule.rb"

def readInput(path)
  rules, ticketMine, ticketsNearby = File.read(path).split("\n\n")
  return rules.split("\n"), ticketMine.split("\n")[1], ticketsNearby.split("\n")[1..-1]
end

def part1 (rules, ticketMine, ticketsNearby)
  rs = RuleSet.new
  for rule in rules
    name, ranges = rule.split(": ")
    range1, range2 = ranges.split(" or ")
    r = Rule.new(name, range1, range2)
    rs.add(r)
  end
  
  errorRate = 0
  for ticket in ticketsNearby
    for value in ticket.split(",")
      if not rs.valid?(value.to_i)
        errorRate += value.to_i
      end
    end
  end
  return errorRate
end


def findFieldNames(tickets, ruleset)
  # first create an Array where each element holds the possible names for the n-th field
  fieldCount = tickets.tickets[0].size
  ticketCount = tickets.tickets.size
  possibleFieldNames = Array.new(fieldCount).map{|v| Array.new}
  for rule in ruleset.rules
    for fieldIx in (0..(fieldCount-1))
      fieldValues = tickets.getField(fieldIx)
      if fieldValues.filter{|v| rule.valid?(v) == true}.size == ticketCount # all tickets are valid
        possibleFieldNames[fieldIx].append(rule.name)
      end
    end
  end

  # sort by possible names and start with the field that only has one option
  #   go through all fields and eliminate previously chosen field names
  fieldNames = Array.new(possibleFieldNames.size)
  sortedWithOriginalIndex = possibleFieldNames
    .map.with_index
    .sort{ |a, b| a[0].size > b[0].size ? 1 : -1 }
  
  for fieldIx in (0..fieldNames.size-1)
    for name in sortedWithOriginalIndex[fieldIx][0]
      if not fieldNames.include?(name)
        fieldNames[sortedWithOriginalIndex[fieldIx][1]] = name
      end
    end
  end
  fieldNames
end

def part2 (rules, ticketMine, ticketsNearby)
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
  names = findFieldNames(validTickets, rs)
  value = 1
  ticketMine = ticketMine.split(",").map(&:to_i)
  for fieldIx in (0..names.size-1)
    fieldName = names[fieldIx]
    if fieldName.include?("departure")
      value *= ticketMine[fieldIx]
    end
  end
  return value
end

if __FILE__ == $PROGRAM_NAME
  rules, ticketMine, ticketsNearby = readInput("./input.txt")
  puts "Solution for part1: %d" % part1(rules, ticketMine, ticketsNearby)
  puts "Solution for part2: #{part2(rules, ticketMine, ticketsNearby)}" # 566, too low, 465416747021 too high, 45145424461037 too high, 268379000107
end