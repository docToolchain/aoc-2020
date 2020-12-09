import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
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

    public fix(){
        if(this.operation === 'jmp') {
            this.operation = 'nop'
        }else if(this.operation === 'nop'){
            this.operation = 'jmp'
        }
    }
}

class Execution{
    public history = new Array<Instruction>()
    public running: boolean = true
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
        if(this.index >= instructions.length){
            this.running = false
        }else{
            const instruction = instructions[this.index]
            this.execute(instruction)
        }
    }
}
                
const instructions = lines.map((line,lineNr) => new Instruction(line,lineNr))

function tryExecution(instructions:Instruction[]):Execution{
    const execution = new Execution()
    do {
        execution.next(instructions)
    } while (execution.running && execution.history.filter(it => it.position === execution.index).length === 0)
    return execution
}

function repair(instructions:Instruction[]):number{
    let fixIndex = 0
    let execution = new Execution()
    do {
        const instructionToFix = instructions[fixIndex]
        if(instructionToFix.operation !== 'acc') {
            instructionToFix.fix()
            execution = tryExecution(instructions)
            instructionToFix.fix() // unfix again
        }
        fixIndex++
    } while (execution?.running === true && fixIndex < instructions.length);
    return execution.acc
}

const result = repair(instructions)

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  