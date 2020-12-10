from pathlib import Path
import re

import copy

class Computer: 

    instructions = []

    accumulator = 0
    pc = 0
    
    def __init__(self, input_file_path):
        self.parse_input_file(input_file_path)

    def parse_input_file(self, input_file_path):
        p = Path(input_file_path)
        
        with p.open() as input_file: 
            for line in input_file:
                instruction = dict()
                instruction["opcode"], instruction["data"] = line.split()
                instruction["data"] = int(instruction["data"])
                self.instructions.append(instruction)

    def check_for_recursion(self):
        executed_instructions = list()

        next_command = self.pc

        while(next_command not in executed_instructions):           
            self.execute_next_instruction()
            executed_instructions.append(next_command)

            next_command = self.pc

            #abort if program counter is outside of instruction list
            if(self.pc > (len(self.instructions) - 1)):
                return False


        return True
        

    def compute_star1(self):
        self.check_for_recursion()            
        return self.accumulator

    def compute_star2(self):


        orig_instructions = copy.deepcopy(self.instructions)

        for line in range(len(orig_instructions)):
            self.instructions = copy.deepcopy(orig_instructions)
              
            self.pc = 0
            self.accumulator = 0

            if self.instructions[line]['opcode'] != "acc":

                if self.instructions[line]['opcode'] == "nop":
                    self.instructions[line]['opcode'] = "jmp"
                else:
                    self.instructions[line]['opcode'] = "nop"                
                
         
            if self.check_for_recursion() == False:
                return self.accumulator            

        return 


    def execute_next_instruction(self):
        instruction = self.instructions[self.pc]

        if instruction["opcode"] == 'acc':
            self.accumlate(instruction["data"])
        elif instruction["opcode"] == 'jmp':
            self.jump(instruction["data"])
        elif instruction["opcode"] == 'nop':
            self.nop()
        else:
            raise Exception('Invalid operand detected!') 

    def accumlate(self, data):
        self.accumulator += data
        self.pc += 1

    def jump(self, data):
        self.pc = self.pc + data

    def nop(self):
        self.pc += 1

if __name__ == "__main__":

    computer = Computer("input.txt")
    print(f"Star 1: Accumulator value: {computer.compute_star1()}")
    print(computer.compute_star2())
    