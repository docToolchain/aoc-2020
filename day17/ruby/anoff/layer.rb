class Layer
  attr_reader :z, :activeFields
  def initialize(z)
    @z = z
    @activeFields = Array.new
    @nextActiveFields = Array.new
  end
  # set this layer to a given state, map is 0,0 based
  def switchTo(map)
    @activeFields = Array.new
    for row, rowIx in map.split("\n").each_with_index
      for value, colIx in row.split("").each_with_index
        if value == "#"
          @activeFields.append(Pos2D.new(colIx, rowIx))
        end
      end
    end
  end
  def active?(x, y)
    p = Pos2D.new(x, y)
    for active in @activeFields
      if active == p
        return true
      end
    end
    return false
  end
  def calcNextState(pocketDimension)
    for field in @activeFields
      
    end
  end
  def applyNextState
    @activeFields = @nextActiveFields
    @nextActiveFields = Array.new
  end
  def xmin
    @activeFields
      .map{|p| p.x}
      .append(0)
      .min
  end
  def xmax
    @activeFields
      .map{|p| p.x}
      .append(0)
      .max
  end
  def ymin
    @activeFields
      .map{|p| p.y}
      .append(0)
      .min
  end
  def ymax
    @activeFields
      .map{|p| p.y}
      .append(0)
      .max
  end
end

class Pos2D
  attr_accessor :x, :y
  def initialize(x, y)
    @x = x
    @y = y
  end

  def ==(o)
    @x == o.x && @y == o.y
  end
end