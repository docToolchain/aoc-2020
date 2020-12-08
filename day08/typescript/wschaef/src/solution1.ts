import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

class Instruction{ 
    public operation: string
    public arg: number
    
    constructor(line:string, public position: number){
        let lineParts = line.split(' ')
        this.operation = lineParts[0]
        this.arg = parseInt(lineParts[1])
    }
}

class Execution{
    public history = new Array<Instruction>()
    constructor(
        public acc: number = 0,
        public index: number = 0
    ){}
    
    public execute(instr: Instruction){
        switch (instr.operation) {
            case 'jmp':
                this.index += instr.arg
                break;
            case 'acc':
                this.acc += instr.arg
            default:
                ++this.index
        }
        this.history.push(instr)
    }
    public next(instructions: Instruction[]){
        const instruction = instructions[this.index]
        this.execute(instruction)
    }
}
                
const instructions = lines.map((line,lineNr) => new Instruction(line,lineNr))
const execution = new Execution()
do {
    execution.next(instructions)
} while (execution.history.filter(it => it.position === execution.index).length === 0);

const result = execution.acc

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  