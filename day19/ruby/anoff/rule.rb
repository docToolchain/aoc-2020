class Rule
  attr_reader :id, :dependencies, :values
  def initialize(string)
    id, rule = string.split(": ")
    @id = id.to_i
    @string = rule
    @isPopulated = false
    @values = Array.new
    @dependencies = rule.scan(/\d+/).map(&:to_i).uniq
  end

  def populate(ruleset)
    for pattern in @string.split(" | ")
      if pattern.include?('"')
        @values.append(pattern.gsub(/"/, ""))
      else
        parts = pattern.split(" ")
        value = ruleset.getRule(parts[0].to_i).values
        parts.delete_at(0)
        while parts.size > 0
          rA = ruleset.getRule(parts[0].to_i)
          value = value.product(rA.values).collect{|x, y| x += y}
          parts.delete_at(0)
        end
        @values += value
      end
    end
    @isPopulated = true
  end
  def populated?
    @isPopulated
  end
end

class RuleSet
  attr_reader :rules
  def initialize
    @rules = Array.new
  end
  def add(rule)
    @rules.append(rule)
    return self
  end
  def populate
    allDependencies = @rules
      .map{|r| r.dependencies}
      .each_with_index
      .sort{|a, b| a[0].size > b[0].size ? 1 : -1}
    populatedRules = Array.new
    while populatedRules.size != @rules.size
      for entry, allDependenciesIx in allDependencies.each_with_index
        curDependencies = entry[0]
        curRuleIx = entry[1]
        allKnown = true
        for d in curDependencies
          if not populatedRules.include?(d)
            allKnown = false
            break
          end
        end
        if allKnown
          r = @rules[curRuleIx]
          r.populate(self)
          populatedRules.append(r.id)
          allDependencies.delete_at(allDependenciesIx)
        end
      end
    end
    return self
  end
  def size
    return @rules.size
  end
  def getRule(id)
    @rules.find{|r| r.id == id}
  end
end