import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n').map(line => parseInt(line)).sort((a,b) => a-b )
lines.unshift(0)
lines.push(lines[lines.length-1] + 3)

const steps = lines.map((el, i) => i === 0 ? 0 : el-lines[i-1]);

const validPerm = [1,1,2,4,7]

let countValid = steps.join(',').split('3,').filter(it => it).map(it => it.split(',').filter(it => it === '1')) // group by "3"
    .map(it => it.length)
    .map(it => validPerm[it])
    .reduce((p,e) => p * e, 1)

const result = countValid

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

