import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
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
    private wpX = 10
    private wpY = 1
    private x = 0
    private y = 0
    constructor(lines: string[]){
        this.instructions = lines.map(line => new Instruction(line.slice(0,1),parseInt(line.slice(1,line.length))))
    }
    public move(instruction:Instruction){
        switch (instruction.action) {
            case 'E':
                this.wpX += instruction.distance
                break;
            case 'N':
                this.wpY += instruction.distance
                break;
            case 'W':
                this.wpX -= instruction.distance
                break;
            case 'S':
                this.wpY -= instruction.distance
                break;
            case 'F':
                const moveX = (this.wpX - this.x) * instruction.distance;
                this.x += moveX
                this.wpX += moveX
                const moveY = (this.wpY - this.y) * instruction.distance;
                this.y += moveY
                this.wpY += moveY
                break;
            case 'R':
                this.turn(instruction.distance)
                break;
            case 'L':
                this.move(new Instruction('R',instruction.distance * -1))
                break;
            default:
                break;
        }
        // console.log(`${this.x}\t${this.y}\t`,`${this.wpX}\t${this.wpY}\t`,instruction)
    }
    private turn(angle:number){
        angle = (angle + 360) % 360
        this.wpX -= this.x
        this.wpY -= this.y
        switch (angle) {
            case 90:
                const tmp1 = this.wpX
                this.wpX = this.wpY
                this.wpY = -1 * tmp1
                break;
            case 180:
                this.wpX = -1 * this.wpX
                this.wpY = -1 * this.wpY
                break;
            case 270:
                const tmp2 = this.wpX
                this.wpX = -1 * this.wpY
                this.wpY = tmp2
                break;
            default:
                break;
        }
        this.wpX += this.x
        this.wpY += this.y
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

