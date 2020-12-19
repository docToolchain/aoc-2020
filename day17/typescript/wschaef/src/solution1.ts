import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const startingPoints = input.split('\n').map(line => line.split(''))

class System{
    public points: Point[]
    private lengthX: number
    private lengthY: number
    private lengthZ: number
    private lowerX: number = 0
    private lowerY: number = 0
    private lowerZ: number = 0
    constructor(points: string[][]){
        this.points = points.map((line,y) => line.map((v,x)=>new Point(x,y,0,v))).flat()
        this.lengthX = points[0].length
        this.lengthY = points.length
        this.lengthZ = 1
    }
    public getNeighbours(point: Point, points: Point[]){
        const range = {
            x:[point.x -1,point.x,point.x +1],
            y:[point.y -1,point.y,point.y +1],
            z:[point.z -1,point.z,point.z +1],
        }
        return points.filter(p => range.x.includes(p.x) 
                        && range.y.includes(p.y) 
                        && range.z.includes(p.z))
                     .filter(p => !(p.x === point.x && p.y === point.y && p.z === point.z))
    }
    private getPoint(x:number,y:number,z:number,points:Point[]){
        let p = points.filter(p => p.x === x && p.y === y && p.z === z)
        const point = p.length > 0 ? p[0] : new Point(x, y, z, '.');
        if(p.length === 0 ) {
            this.points.push(point)
        }
        return point
    }
    private nextValue(p:Point, points: Point[]){
        const countActiveNeighbours = this.getNeighbours(p,points).filter(p => p.v === '#').length
        switch (p.v) {
            case '#':
                p.v = [2,3].includes(countActiveNeighbours) ? '#' : '.'
                break;
            case '.':
                p.v = [3].includes(countActiveNeighbours) ? '#' : '.'
                break;
        }
    }
    public next(){
        this.lengthX += 2
        this.lengthY += 2
        this.lengthZ += 2
        this.lowerX -= 1
        this.lowerY -= 1
        this.lowerZ -= 1
        const copy = this.copyPoints()
        for(let x=this.lowerX; x<this.lengthX-Math.abs(this.lowerX); x++){
            for(let y=this.lowerY; y<this.lengthY-Math.abs(this.lowerY); y++){
                for(let z=this.lowerZ; z<this.lengthZ-Math.abs(this.lowerZ); z++){
                    const p = this.getPoint(x,y,z,this.points)
                    this.nextValue(p,copy)
                }
            }
        }
    }
    public iterate(iterations:number){
        for(let i=0; i<iterations; i++){
            this.next()
        }
    }
    private copyPoints():Point[]{
        return this.points.map(p=> ({...p}) as Point)
    }
    public print(){
        let result = new Array<Array<string>>()
        for(let z=this.lowerZ; z<this.lengthZ-Math.abs(this.lowerZ); z++){
            let block = []
            for(let y=this.lowerY; y<this.lengthY-Math.abs(this.lowerY); y++){
                let line = ''
                for(let x=this.lowerX; x<this.lengthX-Math.abs(this.lowerX); x++){
                    const p = this.getPoint(x,y,z,this.points)
                    line = line.concat(p.v)
                }
                block.push(line+'         -----------')
            }
            result.push(block)
        }
        console.log(result)
    }
}

class Point{
    constructor(
        public x: number,
        public y: number,
        public z: number,
        public v: string){  
    }
}

const system = new System(startingPoints)
system.iterate(6)
system.print()
const result = system.points.filter(p=>p.v === '#').length
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
