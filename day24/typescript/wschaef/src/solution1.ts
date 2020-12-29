import * as fs from 'fs';
import { log } from 'util';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n').map(line => parseLine(line));

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

// const points3d = lines.map(line => line.reduce((p,it) => turn(it,p),[0,0,0]))
// const points2d = points3d.map(([x,y,z])=>[x+z,y-z])
// const counts = points2d.reduce((counts,p) => counts.set(p.toString(), (counts.get(p.toString())||0)+1),new Map<string,number>())

// const result = Array.from(counts).filter(it=> it[1] %2 === 1).length
// console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 