import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
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

function checkContiquousSet(entries: number[],pos:number,value:number){
    let sum = 0
    let listOfEntries: number[] = []
    for (const entry of entries.slice(pos)) {
        if(sum < value){
            sum = sum + entry
            listOfEntries.push(entry)
            if(sum === value){
                return Math.max(...listOfEntries) + Math.min(...listOfEntries)
            }
        }else{
            break;
        }
    }
    return 0
}

function findContiguousSet(){
    for(let i=0; i<lines.length; i++){
        const checkResult = checkContiquousSet(lines, i, invalidNumber);
        if(checkResult > 0){
            return checkResult
        }
    }
    return 0
}

const invalidNumber = findInvalidEntry(lines)
const result = findContiguousSet()

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

