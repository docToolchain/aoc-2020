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

class Seatmap2
  attr_reader :map
  attr_writer :map
  def initialize(map)
    @map = map
  end
  def occupiedSeatCount(x, y)
    count = 0
    dirs = [
      [-1, 0],
      [-1, -1],
      [0, -1],
      [+1, -1],
      [+1, 0],
      [+1, +1],
      [0, +1],
      [-1, +1]
    ]
    for dir in dirs
      x1, y1 = self.getNextSeat(x, y, dir[0], dir[1])
      if self.occupied?(x1, y1)
        count += 1
      end
    end
    return count
  end

  # walk into direction specified by xD/yD until you reach the next available seat
  def getNextSeat(x0, y0, xD, yD)
    x = x0 + xD
    y = y0 + yD
    while !self.isSeat?(x, y)
      x = x + xD
      y = y + yD
      if !self.withinRange?(x, y)
        return [-1, -1]
      end
    end
    return [x, y]
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
        if self.isSeat?(x, y) && self.occupied?(x, y) && self.occupiedSeatCount(x, y) >= 5
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