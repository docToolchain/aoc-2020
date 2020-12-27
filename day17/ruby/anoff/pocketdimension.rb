class PocketDimension
  attr_reader :xmin, :xmax, :ymin, :ymax
  def initialize
    @layers = Array.new
    @xmin = 0
    @xmax = 0
    @ymin = 0
    @ymax = 0
    @neighborMap = Array.new
    @activeFields = Array.new
  end
  def addLayer(layer)
    @layers.append(layer)
  end
  def getLayer(z)
    for l in @layers
      if l.z == z
        return l
      end
    end
    return nil
  end
  def getNeighbors(x, y, z)
    neighborCount = 0
    z0 = self.getLayer(z)
    neighborCount += z0.active?(x+1, y) ? 1 : 0
    neighborCount += z0.active?(x+1, y+1) ? 1 : 0
    neighborCount += z0.active?(x+1, y-1) ? 1 : 0
    neighborCount += z0.active?(x, y+1) ? 1 : 0
    neighborCount += z0.active?(x, y-1) ? 1 : 0
    neighborCount += z0.active?(x-1, y) ? 1 : 0
    neighborCount += z0.active?(x-1, y+1) ? 1 : 0
    neighborCount += z0.active?(x-1, y-1) ? 1 : 0
    zp = self.getLayer(z+1)
    if not zp.nil?
      neighborCount += zp.active?(x+1, y) ? 1 : 0
      neighborCount += zp.active?(x+1, y+1) ? 1 : 0
      neighborCount += zp.active?(x+1, y-1) ? 1 : 0
      neighborCount += zp.active?(x, y) ? 1 : 0
      neighborCount += zp.active?(x, y+1) ? 1 : 0
      neighborCount += zp.active?(x, y-1) ? 1 : 0
      neighborCount += zp.active?(x-1, y) ? 1 : 0
      neighborCount += zp.active?(x-1, y+1) ? 1 : 0
      neighborCount += zp.active?(x-1, y-1) ? 1 : 0
    end
    zn = self.getLayer(z-1)
    if not zn.nil?
      neighborCount += zn.active?(x+1, y) ? 1 : 0
      neighborCount += zn.active?(x+1, y+1) ? 1 : 0
      neighborCount += zn.active?(x+1, y-1) ? 1 : 0
      neighborCount += zn.active?(x, y) ? 1 : 0
      neighborCount += zn.active?(x, y+1) ? 1 : 0
      neighborCount += zn.active?(x, y-1) ? 1 : 0
      neighborCount += zn.active?(x-1, y) ? 1 : 0
      neighborCount += zn.active?(x-1, y+1) ? 1 : 0
      neighborCount += zn.active?(x-1, y-1) ? 1 : 0
    end
    return neighborCount
  end

  def cycle
    self.updateRange
    for z, ix in @neighborMap.each_with_index
      l = self.getLayer(ix + @zmin)
      for field in l.activeFields
        z[field.y][field.x+1] += 1
        z[field.y+1][field.x+1] += 1
        z[field.y-1][field.x+1] += 1
        z[field.y+1][field.x] += 1
        z[field.y-1][field.x] += 1
        z[field.y][field.x-1] += 1
        z[field.y+1][field.x-1] += 1
        z[field.y-1][field.x-1] += 1
        if ix > 0
          @neighborMap[ix-1][field.y][field.x+1] += 1
          @neighborMap[ix-1][field.y+1][field.x+1] += 1
          @neighborMap[ix-1][field.y-1][field.x+1] += 1
          @neighborMap[ix-1][field.y][field.x] += 1
          @neighborMap[ix-1][field.y+1][field.x] += 1
          @neighborMap[ix-1][field.y-1][field.x] += 1
          @neighborMap[ix-1][field.y][field.x-1] += 1
          @neighborMap[ix-1][field.y+1][field.x-1] += 1
          @neighborMap[ix-1][field.y-1][field.x-1] += 1
        end
        if ix < @neighborMap.size-1
          @neighborMap[ix+1][field.y][field.x+1] += 1
          @neighborMap[ix+1][field.y+1][field.x+1] += 1
          @neighborMap[ix+1][field.y-1][field.x+1] += 1
          @neighborMap[ix+1][field.y][field.x] += 1
          @neighborMap[ix+1][field.y+1][field.x] += 1
          @neighborMap[ix+1][field.y-1][field.x] += 1
          @neighborMap[ix+1][field.y][field.x-1] += 1
          @neighborMap[ix+1][field.y+1][field.x-1] += 1
          @neighborMap[ix+1][field.y-1][field.x-1] += 1
        end
      end
    end

    for z, ix in @neighborMap.each_with_index
      l = self.getLayer(ix + @zmin)
      @activeFields...
    end
  end
  def updateRange
    @xmin = 10e3
    @xmax = 0
    @ymin = 10e3
    @ymax = 0
    @zmin = 10e3
    @zmax = 0
    for layer in @layers
      @xmin = [@xmin, layer.xmin].min
      @xmax = [@xmax, layer.xmax].max
      @ymin = [@ymin, layer.ymin].min
      @ymax = [@ymax, layer.ymax].max
      if layer.activeFields.size > 0
        @zmin = [@zmin, layer.z].min
        @zmax = [@zmax, layer.z].max
      end
    end
    if self.getLayer(@zmin-1).nil?
      l = Layer.new(@zmin-1)
      self.addLayer(l)
    end
    if self.getLayer(@zmax+1).nil?
      l = Layer.new(@zmax+1)
      self.addLayer(l)
    end
    @xmin -= 1
    @xmax += 1
    @ymin -= 1
    @ymax += 1
    @neighborMap = # [z][y][x]
      Array.new(@zmax-@zmin+1) # z-level
      .map {|z|
        Array.new(@ymax-@ymin+1) # y
        .map{|y| Array.new(@xmax-@xmin+1).fill(0)} # x
      }
  end
  def print
    for l in @layers
      if l.activeFields.size == 0
        next
      end
      puts ""
      puts "z=#{l.z}"
      for y in (@ymin..@ymax)
        line = Array.new
        for x in (@xmin..@xmax)
          line.append(l.active?(x, y) ? "#" : ".")
        end
        puts line.join("")
      end
    end
  end
  def activeCount
    count = 0
    for l in @layers
      count += l.activeFields.size
    end
    return count
  end
end
