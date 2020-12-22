require "test/unit"
require_relative './solution'

class TestSolution < Test::Unit::TestCase
  def Ttest_cycleVisual
    map = readInput("./input_test.txt")
    pd = PocketDimension.new
    l = Layer.new(0)
    l.switchTo(map)
    pd.addLayer(l)
    puts "t=0"
    pd.print
    puts "t=1"
    pd.cycle
    pd.print
    puts "t=2"
    pd.cycle
    pd.print
  end
  def test_cycle
    map = readInput("./input_test.txt")
    pd = PocketDimension.new
    l = Layer.new(0)
    l.switchTo(map)
    pd.addLayer(l)
    for i in 1..6
      pd.cycle
    end
    assert_equal 112, pd.activeCount
  end
end