import * as fs from 'fs';
import { isMainThread } from 'worker_threads';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n\n').map(it=>it.split('\n').slice(1).map(it=>parseInt(it)))

function round(decks:number[][]):number[][]{
    const cardsOnTable = decks.map(deck => deck.shift() as number)
    const max = cardsOnTable.reduce((m,it)=> Math.max(m,it),0)
    const player = cardsOnTable.findIndex(it => it === max)
    decks[player] = [...decks[player],...cardsOnTable.sort((a,b)=> b-a)]
    return decks
}
function game(decks:number[][]):number[][]{
    if(decks.some(it => it.length === 0)){
        return decks
    }
    const result = round(decks)
    return game(result)
}

const result = game(lines).filter(it=>it.length >0)[0].reverse().map((it,i)=>it*(i+1)).reduce((s,it)=>s+it,0)
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 