package cpu

class Vm {
    static state = [pointer:0, acc:0]
    static program = []
    static void run() {
        while (1==1) {
            def current = program[state.pointer] 
            if (current==null) {
                throw new Exception("terminated with acc="+state.acc)
            }
            if (program[state.pointer]['visited']!=null) {
                throw new Exception("endless loop with acc="+state.acc)
            }
            program[state.pointer]['visited'] = state.pointer
            switch (current.op) {
                case 'nop':
                    // nop stands for No OPeration - it does nothing. 
                    // The instruction immediately below it is executed next.
                    state.pointer++
                    break;
                case 'acc':
                    // acc increases or decreases a single global value called 
                    // the accumulator by the value given in the argument. 
                    // For example, acc +7 would increase the accumulator by 7. 
                    // The accumulator starts at 0. After an acc instruction, 
                    // the instruction immediately below it is executed next.
                    state.acc += current.p1
                    state.pointer++
                    break;
                case 'jmp':
                    // jmp jumps to a new instruction relative to itself. 
                    // The next instruction to execute is found using the 
                    // argument as an offset from the jmp instruction; 
                    // for example, jmp +2 would skip the next instruction, 
                    // jmp +1 would continue to the instruction immediately below it, 
                    // and jmp -20 would cause the instruction 20 lines above to be executed next.
                    state.pointer += current.p1
                    break;
            }
        }
    }
}