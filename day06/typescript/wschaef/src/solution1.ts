import * as fs from 'fs';

const input = fs.readFileSync('input1.txt','utf8');
let answers = input.split('\n\n').map(line => line.split('\n').join(" "))

function countYes(answer:string): number{
    answer = answer.replace(/ /ig,'')
    const entries = [...new Set(answer.split(''))].join("")
    return entries.length
}

let result = answers.map(p => countYes(p)).reduce((sum,el)=>sum+el,0)
console.log(result)