class Computer
  attr_reader :acc, :ptrHistory
  def initialize(operations)
    @operations = operations
    @acc = 0
    @ptr = 0
    @ptrHistory = []
  end

  def step
    if @ptrHistory.include?(@ptr)
      # puts "Infinite Execution detected. Program trying to execute command##{@ptr} a second time"
      return -1
    end
    @ptrHistory.append(@ptr)
    if @ptr >= @operations.size - 1
      # puts "End of Program reached"
      return 1
    end
    op = @operations[@ptr]
    code, value = op.split(" ")
    value = value.to_i
    case code
      when "nop"
        @ptr += 1
      when "acc"
        @acc += value
        @ptr += 1
      when "jmp"
        @ptr += value
      else
        puts "Unknown operation detected: #{op}"  
        return -1
    end
    return 0
  end

  def run
    code = 0
    while code == 0
      code = self.step
    end
    return code
  end
end