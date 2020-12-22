class Rule
  attr_reader :name, :validValues
  def initialize(name, range1, range2)
    def getValuesFromRange(range)
      values = []
      min, max = range.split("-")
      return (min.to_i .. max.to_i).to_a
    end
    @name = name
    @validValues = getValuesFromRange(range1) + getValuesFromRange(range2)
  end

  def valid?(value)
    return @validValues.include?(value)
  end
end

class RuleSet
  attr_reader :rules, :validValues
  def initialize
    @rules = Array.new
    @validValues = Array.new
  end
  def add(rule)
    @rules.append(rule)
    @validValues += rule.validValues
    @validValues = @validValues.uniq
    return self
  end
  def valid?(value)
    return @validValues.include?(value)
  end
  def size
    return @rules.size
  end
end

class Tickets
  attr_reader :tickets
  def initialize
    @tickets = []
    @ticketSize = 0
  end
  def add(ticket)
    @tickets.append(ticket.split(",").map(&:to_i))
    if @ticketSize == 0
      @ticketSize = @tickets[0].size
    end
  end
  def getField(n)
    values = Array.new(@tickets.size)
    for i in (0..(@tickets.size-1))
      values[i] = @tickets[i][n]
    end
    return values
  end
end