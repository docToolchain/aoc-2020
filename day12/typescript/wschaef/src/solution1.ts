import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')


class Instruction{
    constructor(
        public action: string,
        public distance: number
    ){}
}
class Trip{
    public instructions: Instruction[]
    private x = 0
    private y = 0
    private direction : string = 'E'
    private angles = ['N','E','S','W']
    constructor(lines: string[]){
        this.instructions = lines.map(line => new Instruction(line.slice(0,1),parseInt(line.slice(1,line.length))))
    }
    public move(instruction:Instruction){
        switch (instruction.action) {
            case 'E':
                this.x += instruction.distance
                break;
            case 'N':
                this.y += instruction.distance
                break;
            case 'W':
                this.x -= instruction.distance
                break;
            case 'S':
                this.y -= instruction.distance
                break;
            case 'F':
                this.move(new Instruction(this.direction,instruction.distance))
                break;
            case 'R':
                let angle = this.angles.findIndex(it => it === this.direction)
                angle = (angle + instruction.distance/90 + 4) % 4 // +4 because of modulo bug in js
                this.direction = this.angles[angle]
                break;
            case 'L':
                this.move(new Instruction('R',instruction.distance * -1))
                break;
            default:
                break;
        }
    }
    public travel(){
        this.instructions.forEach(instruction => this.move(instruction))
    }

    public getManhattanDistance(){
        console.log(this.x,this.y) 
        return Math.abs(this.x) + Math.abs(this.y)
    }
}

const trip = new Trip(lines)
trip.travel()
const result = trip.getManhattanDistance()

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

