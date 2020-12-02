import * as fs from 'fs';
const input = fs.readFileSync('input1.txt','utf8');

const lines = input.split('\n');

let valueList = lines
.map((line: string) => parseInt(line))


let check = (): number => {
    for (let n of valueList){
        for (let m of valueList){
            if(n+m===2020){
                return n*m;
            }
        } 
    };
}

let result = check()
console.log(result)