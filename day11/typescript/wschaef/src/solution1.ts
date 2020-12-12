import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

class Layout{
    public layout: string[][]
    constructor(private lines: string[]){
        this.layout = lines.map(line => line.split(''))
    }
    private getNeighbours(x:number, y:number, layout: string[][]):string[]{
        const neighbourIndexes = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]
        const neighbours = neighbourIndexes.map(it => layout[it[1]]?.[it[0]]).filter(it=>it)
        return neighbours
    }
    private getNextValue(x:number, y:number, layout: string[][]){
        const seatValue = layout[y][x]
        let result = seatValue
        if(seatValue !== '.'){
            const neighbours = this.getNeighbours(x,y,layout)
            switch (seatValue) {
                case 'L':
                    if(neighbours.filter(it => it === '#').length === 0) result = '#' 
                    break;
                case '#':
                    if(neighbours.filter(it => it === '#').length > 3) result = 'L' 
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
for(let i=0; i<10000000; i++){
    if(layout.next()){
        break
    }
}

const result = layout.layout.flat().filter(it => it === '#').length

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

