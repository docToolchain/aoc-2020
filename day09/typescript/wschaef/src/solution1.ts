import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n').map(line => parseInt(line))

const PREAMBLE_SIZE = 25

function getValidEntries(entries: number[], pos:number){
    const preamble = entries.slice(pos-PREAMBLE_SIZE,pos)
    const result = preamble.map(p => preamble.slice(1).map(q => p+q)).flat()
    return result
}


function findInvalidEntry(entries:number[]) {
    let result = 0
    entries.some((line: number, index) => {
        if (index >= PREAMBLE_SIZE) {
            if (!getValidEntries(entries, index).includes(line)) {
                result = line
                return line
            }
        }
    });
    return result
}

const result = findInvalidEntry(lines); 

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

