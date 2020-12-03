import * as fs from 'fs';
const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n');

let check = (line: string):boolean => {
    const [rule,password] = line.split(":")
    const [validPositions,letter] = rule.split(' ')
    const passwordArray = password.split('')
    const numberOfLetters = validPositions.split('-')
        .map(pos => password.charAt(parseInt(pos))===letter?1:0)
        .reduce((sum:number,elem:number) => sum + elem,0) 
    return numberOfLetters === 1
}

let result = lines.filter(line => check(line)).length
console.log(result)