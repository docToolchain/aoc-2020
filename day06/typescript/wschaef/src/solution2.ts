import * as fs from 'fs';

const input = fs.readFileSync('input1.txt','utf8');
let answers = input.split('\n\n').map(line => line.split('\n'))

function countYes(groupAnswers:string[]): number{
    const result = groupAnswers.map(it => it.split(''))
        .reduce((a, b) => a.filter(c => b.includes(c)))
    return result.length
}

let result = answers.map(p => countYes(p)).reduce((sum,el)=>sum+el,0)
console.log(result)