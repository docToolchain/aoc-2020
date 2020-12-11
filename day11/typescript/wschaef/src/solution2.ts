import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

class Layout{
    public layout: string[][]
    constructor(private lines: string[]){
        this.layout = lines.map(line => line.split(''))
    }
    private getNumberOfNeighbours(x:number, y:number, layout: string[][]):number{
        const maxX = layout[0].length
        const maxY = layout.length
        const maxDistance = Math.max(maxX,maxY)
        let directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]] 
        let result = directions.map(it => this.isSeatInDirection(x,y,it[0],it[1],layout))
        return result.filter(it=>it).length
    }

    private isSeatInDirection(x:number,y:number,xd:number,yd:number,layout:string[][]):boolean{
        let value = ''
        let currentX = x
        let currentY = y 
        do {
            currentX += xd
            currentY += yd
            value = layout[currentY]?.[currentX]
        } while (value !== undefined && !['L','#'].includes(value));
        return value === '#'
    }

    private getNextValue(x:number, y:number, layout: string[][]){
        const seatValue = layout[y][x]
        let result = seatValue
        if(seatValue !== '.'){
            const neighbours = this.getNumberOfNeighbours(x,y,layout)
            switch (seatValue) {
                case 'L':
                    if(neighbours === 0) result = '#' 
                    break;
                case '#':
                    if(neighbours > 4) result = 'L' 
                    break;
            }
        }
        return result
    }

    public next(): boolean{
        const snapshot = this.layout.map(it => it.slice())
        this.layout = this.layout.map((line,y) => line.map((elem,x) => this.getNextValue(x,y,snapshot)))
        return snapshot.toString() === this.layout.toString()
    }

}
const layout = new Layout(lines)
for(let i=0; i<1000000; i++){
    if(layout.next()){
        break
    }
}

const result = layout.layout.flat().filter(it => it === '#').length

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

