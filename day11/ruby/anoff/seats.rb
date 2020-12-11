class Seatmap
  attr_reader :map
  attr_writer :map
  def initialize(map)
    @map = map
  end
  def occupiedSeatCount(x, y)
    count = 0
    count += self.occupied?(x-1, y) ? 1 : 0
    count += self.occupied?(x-1, y-1) ? 1 : 0
    count += self.occupied?(x, y-1) ? 1 : 0
    count += self.occupied?(x+1, y-1) ? 1 : 0
    count += self.occupied?(x+1, y) ? 1 : 0
    count += self.occupied?(x+1, y+1) ? 1 : 0
    count += self.occupied?(x, y+1) ? 1 : 0
    count += self.occupied?(x-1, y+1) ? 1 : 0
    return count
  end

  def occupied?(x, y)
    if not self.withinRange?(x, y)
      return false
    end
    return map[y][x] == "#" ? true : false
  end

  # print seatmap
  def print
    for line in @map
      puts line.join("")
    end
  end

  def setOccupied(x, y, isOccupied)
    if withinRange?(x, y)
      line = @map[y]
      line[x] = isOccupied ? "#" : "L"
    else
      puts "not in range"
    end
  end

  def isSeat?(x, y)
    if not self.withinRange?(x, y)
      return false
    end
    line = @map[y]
    if line[x] == "."
      return false
    end
    return true
  end

  def withinRange?(x, y)
    return !(x < 0 || y < 0 || y > map.size - 1 || x > map[0].size - 1)
  end

  # run simulation step over the entire seatmap
  def step
    t = Seatmap.new(Marshal.load(Marshal.dump(@map))) # deep copy
    for y in (0..(@map.size - 1))
      for x in (0..(@map[0].size - 1))
        if self.isSeat?(x, y) && !self.occupied?(x, y) && self.occupiedSeatCount(x, y) == 0
          t.setOccupied(x, y, true)
        end
        if self.isSeat?(x, y) && self.occupied?(x, y) && self.occupiedSeatCount(x, y) >= 4
          t.setOccupied(x, y, false)
        end
      end
    end
    @map = Marshal.load(Marshal.dump(t.map))
  end

  def totalOccupiedSeatCount
    @map
      .map{ |line| line.filter{ |c| c == "#" }}
      .map{ |line| line.size}
      .reduce(&:+)
  end
end