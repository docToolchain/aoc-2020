class Ruleset
  attr_reader :bags
  def initialize(rules)
    @bags = []
    for rule in rules
      color, contents = rule.split(" bags contain ")
      contents = contents.gsub(/\sbag(s)?/, '').gsub(/\./, '')
      b = Bag.new(color, contents.split(", "))
      @bags.append(b)
    end
  end
  def getBag(color)
    res = @bags.filter{|b| b.color == color}
    if res.size == 1
      return res[0]
    else
      puts "Could not find bag of color #{color}"
    end
  end
  def expandRules
    for b in @bags
      b.expandRules(self)
    end
  end
end

class Bag
  attr_reader :color, :rules, :contents, :contentSize
  def initialize(color, rules)
    @color = color
    @rules = rules
    @contents = []
    @contentSize = 0
    @isExpanded = false
  end

  def expanded?
    return @isExpanded
  end

  def canContain?(color)
    @contents
      .filter {|b| b.color == color}
      .size >= 1
  end

  def expandRules(ruleset)
    if @isExpanded
      return
    end
    for rule in @rules
      if rule == "no other"
        next
      end
      bagCount = rule.split(" ")[0].to_i
      bagColor = rule.gsub(/[0-9]+\s?/, '')
      b = ruleset.getBag(bagColor)
      if not b.expanded?
        b.expandRules(ruleset)
      end
      @contents += b.contents
      @contents.append(b)
      for n in 1..bagCount
        @contentSize += b.contentSize
        @contentSize += 1
      end
    end
    @isExpanded = true
  end


end