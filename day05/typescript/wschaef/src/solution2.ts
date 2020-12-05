import * as fs from 'fs';

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n')

function getSeat(line :string){
    const rowStr = line.substr(0,line.length-3)
            .replace(/F/g,"0").replace(/B/g,"1")
    const row = parseInt(rowStr,2)      
    const colStr = line.substr(line.length-3,3)
            .replace(/L/g,"0").replace(/R/g,"1")
    const col = parseInt(colStr,2)
    return row*8+col
}

const seats = lines.map(line => getSeat(line)).sort((n1,n2) => n1 - n2);

function findMySeat(seats: number[]){
    for(let i=0; i<seats.length-1; i++){
        if((seats[i+1] - seats[i])>1){
            return seats[i]+1
        }
    }
    return 0
}
let result = findMySeat(seats)
console.log(result)
