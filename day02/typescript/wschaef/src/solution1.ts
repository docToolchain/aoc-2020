import * as fs from 'fs';
const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n');

let check = (line: string):boolean => {
    const [rule,password] = line.split(":")
    const [range,letter] = rule.split(' ')
    const [min,max] = range.split('-').map(it => parseInt(it))
    const countLetter = password.split('').filter(it => it===letter).length
    return min <= countLetter && countLetter <= max
}

let result = lines.filter(line => check(line)).length
console.log(result)