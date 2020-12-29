import * as fs from 'fs';
import { uniqBy, cloneDeep } from 'lodash-es' 

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n').map(line => parseLine(line));

class Field{
    public id: string
    constructor(public black: boolean,public x : number, public y : number ){
        this.id = [this.x,this.y].join('|')
    }
}

class Floor{

    private registry : Map<string,Field>
    constructor(public fields = new Array<Field>()){
        this.registry = new Map<string,Field>()
        this.fields.reduce((reg,f) => reg.set(f.id,f),this.registry)
    }

    public setFields(fields: Array<Field>){
        this.fields = fields
        this.fields.reduce((reg,f) => reg.set(f.id,f),this.registry)
    }

    public getField(x:number,y:number):Field{
        return this.registry.get([x,y].join('|')) || new Field(false,x,y)
    }
    
    public getNeighbors(field:Field):Field[]{
        const [x,y] = [field.x,field.y]
        const coordinates =  [[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y-1],[x-1,y+1]]
        return coordinates.map(c => this.registry.get(c.join('|')) || new Field(false, c[0], c[1]))
    }

    public flip(field: Field, countBlackNeighbours:number): void{
        switch (field.black) {
            case true:
                if(countBlackNeighbours === 0 || countBlackNeighbours > 2)
                field.black = false
                break;
            case false:
                if(countBlackNeighbours === 2)
                    field.black = true
                break;
            default:
                break;
        }
    }

    public nextDay(){
        this.fields = this.fields.filter(f => f.black)
        const extendedFields = cloneDeep(uniqBy([...this.fields,...this.fields.map(f => this.getNeighbors(f)).flat()],(it => it.id)))
        const newFields = new Map<string,Field>() 
        extendedFields.forEach(field => {
            const neightbours = this.getNeighbors(field)
            const blacks = neightbours.filter(it => it.black).length
            this.flip(field,blacks)
            neightbours.forEach(n => {if(!newFields.has(n.id)) {newFields.set(n.id,n)}}) 
            newFields.set(field.id, field)

        })
        this.setFields([...newFields.values()])
        return this
    }
    public countBlacks(){
        return this.fields.filter(f => f.black).length
    }

    public print(){
        const xValues = this.fields.map(it => it.x)
        const yValues = this.fields.map(it => it.y)
        const [xMin,xMax] = [Math.min(...xValues),Math.max(...xValues)]
        const [yMin,yMax] = [Math.min(...yValues),Math.max(...yValues)]
        let result = [yMax -yMin][xMax-xMin]
        console.log(xMin,xMax)
        console.log('\t | ' + Array.from(Array(xMax-xMin+1).keys()).map(it => (it + xMin).toString().padStart(2)).join(' | '))
        console.log('------------------------------------------')
        for(let y = yMin; y<=yMax; y++){
            const line = [y.toString() + '\t']
            for(let x = xMin; x <= xMax; x++){
                if(this.fields.find(it => it.x === x && it.y ===y)?.black){
                    line.push('#'.padStart(2))
                }else{
                    line.push('.'.padStart(2))
                }
            }
            console.log(line.join(' | '))
        }
    }
}

function parseLine(line:string):string[] {
    const result = new Array<string>()
    let elem = new Array<string>()
    line.split('').forEach((char,i) => {
        if(['n','s'].includes(char)){
            elem.push(char)
        }else{
            if(elem.length === 0){
                result.push(char)
            }else{
                elem.push(char)
                result.push(elem.join(''))
                elem = []
            }
        }
    });
    return result
}

function turn(instruction:string,point:number[]):number[]{
    switch (instruction) {
        case 'ne':
            point[1]++
            break;
        case 'e':
            point[0]++
            break;
        case 'se':
            point[2]++
            break;
        case 'sw':
            point[1]--
            break;
        case 'w':
            point[0]--
            break;
        case 'nw':
            point[2]--
            break;
        default:
            break;
    }
    return point
}




const points3d = lines.map(line => line.reduce((p,it) => turn(it,p),[0,0,0]))
const points2d = points3d.map(([x,y,z])=>[x+z,y-z])
const counts = points2d.reduce((counts,p) => counts.set(p.toString(), (counts.get(p.toString())||0)+1),new Map<string,number>())
const fields = Array.from(counts).map(([p,count]) => [count,...p.split(',').map(Number)])
                                 .map(([count,x,y])=> new Field((count % 2 === 1),x,y))
const floor = new Floor(fields)
for(let i=0; i < 100; i++){
    floor.nextDay()
    // console.log('Round:', i+1,' blacks: ', floor.countBlacks())
}
// floor.print();

const result = floor.countBlacks()
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 