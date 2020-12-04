import * as fs from 'fs';

const input = fs.readFileSync('input1.txt','utf8');
let passports = input.split('\n\n').map(line => line.split('\n').join(" "))

function validate(passport:string): boolean{
    const entries = passport.split(" ")
    const fields = entries.map(entry => entry.split(":")[0])
    const requiredFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid']
    const result = requiredFields.every(field => fields.includes(field))
    return result
}

let result = passports.map(p => validate(p)).filter(it => it).length
console.log(result)
