import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n').map(line => parseInt(line)).sort((a,b) => a-b )
lines.unshift(0)
lines.push(lines[lines.length-1] + 3)

const steps = lines.map((el, i) => i === 0 ? 0 : el-lines[i-1]);
const result = [1,3].map(x => steps.filter(it => it === x).length).reduce((prod,el) => el * prod,1)

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

