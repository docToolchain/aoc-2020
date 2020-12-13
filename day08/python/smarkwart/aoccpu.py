import copy

class AoCCPU:
    """
    A class for the Advent of Code CPU
    """
    
    def __init__(self, program_listing):
        """
        docstring
        """
        self.reset()
        self.program = copy.deepcopy(program_listing)


    def reset(self):
        """
        docstring
        """
        self.program_counter = 0
        self.accumulator = 0
        self.opcode = ""
        self.operand = 0
        self.execution_graph = []

    def __decode_instruction(self, instruction):
        """
        decodes the instruction into opcode and operand
        """
        self.opcode = instruction.get('opcode')
        self.operand = int(instruction.get('operand'))

    def __execute_instruction(self):
        """
        executes the instructions
        """
        #print(f"\t{self.program_counter}\t{self.accumulator}\t{self.opcode}\t{self.operand}")
        if self.opcode == 'acc':
            self.accumulator += self.operand
            self.program_counter += 1
        elif self.opcode == 'jmp':
            self.program_counter += self.operand
        else:
            self.program_counter += 1
        return

    def __loop_detected(self):
        """
        docstring
        """
        if self.program_counter in self.execution_graph:
            return True

    def restart(self):
        """
        docstring
        """
        #print(f"\n\tpc\tacc\top\topc")
        self.reset()
        return self.start()

    def start(self):
        """
        docstring
        """
        while self.program_counter < len(self.program):
            self.__decode_instruction(self.program[self.program_counter])
            if self.__loop_detected():
                return "LOOP_DETECTED"
            self.execution_graph.append(self.program_counter)
            self.__execute_instruction()
        return "COMPLETED"

    def load_program(self, program_listing):
        """
        docstring
        """
        self.program = copy.deepcopy(program_listing)
        
    def get_accumulator(self):
        """
        docstring
        """
        return self.accumulator

    def get_execution_graph(self):
        """
        docstring
        """
        return self.execution_graph
