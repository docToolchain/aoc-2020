import * as fs from 'fs';
const input = fs.readFileSync('input1.txt','utf8');

const lines = input.split('\n');

let valueList = lines
.map((line: string) => parseInt(line))

let result
for (let n of valueList){
    for (let m of valueList){
        for (let l of valueList){
            if(n+m+l===2020){
                result = n*m*l;
                break;
            }
        }
    } 
};

console.log(result)
