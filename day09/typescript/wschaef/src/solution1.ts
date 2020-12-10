import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n').map(line => parseInt(line))

const PREAMBLE_SIZE = 25

function isValidEntry(entries: number[], pos:number, entry:number){
    const preamble = entries.slice(pos,pos+PREAMBLE_SIZE)
    const result = preamble.some((p,i) => preamble.slice(1+i).some(q => p+q === entry))
    return result
}


function findInvalidEntry(entries:number[]) {
    let result = 0
    entries.slice(PREAMBLE_SIZE).some((entry: number, index) => {
        if (!isValidEntry(entries, index,entry)) {
            result = entry
            return true
        }
    });
    return result
}

const result = findInvalidEntry(lines); 

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

