import * as fs from 'fs';
import { log } from 'util';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n\n').map(it=>it.split('\n').slice(1).map(it=>parseInt(it)))

const round = (p1:number[],p2:number[]) => {
    console.assert([p1,p2].every(p => p.length>0))
    const c1 = p1.shift() as number //p1.length is always > 0 
    const c2 = p2.shift() as number //p2.length is always > 0 
    let winner : number = NaN
    if( c1 <= p1.length && c2 <= p2.length){
        const res = game(p1.slice(0,c1),p2.slice(0,c2))
        winner = res.winner
    }else{
        winner = c1 > c2 ? 1 : 2
    }
    if(winner === 1){
        p1.push(c1,c2)
    }else{
        p2.push(c2,c1)
    }
    return {p1,p2,winner}
}

let gameIndex = 0
const game = (p1:number[],p2:number[]) => {
    gameIndex++
    const prev = new Map<string,boolean>()
    let winner : number = NaN
    while (![1,2].includes(winner)) {
        const prevKey = [p1,p2].map(p => p.toString()).join(' ')
        if(prev.has(prevKey)){
            winner = 1
        }else{
            const res = round(p1,p2)
            p1 = res.p1
            p2 = res.p2
            if([p1,p2].some(p => p.length === 0)){
                winner = res.winner
            }
        }
        prev.set(prevKey,true)
    }
    return {p1,p2,winner}
}

const score = (p:number[]) => {
    return p.reverse().map((it,i)=>it*(i+1)).reduce((s,it)=>s+it,0)
}

const g = game(lines[0],lines[1])

const result = score(g.winner === 1 ? g.p1 : g.p2)
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")
 