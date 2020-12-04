import * as fs from 'fs';

const input = fs.readFileSync('input1.txt','utf8');
let passports = input.split('\n\n').map(line => line.split('\n').join(" "))

function validate(passport:string): boolean{
    const entries = passport.split(" ")
    const fieldNames = entries.map(entry => entry.split(":")[0])
    const requiredFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid']
    let valid = requiredFields.every(field => fieldNames.includes(field))
    if(valid){
        const fields = entries.map(entry => entry.split(":") as [string, string])
        const passObj = new Map<string,string>(fields)
        
        const byr = parseInt(passObj.get('byr') || '0')
        valid = valid && byr >= 1920 && byr <= 2002
        
        const iyr = parseInt(passObj.get('iyr') || '0')
        valid = valid && iyr >= 2010 && iyr <= 2020
        
        const eyr = parseInt(passObj.get('eyr') || '0')
        valid = valid && eyr >= 2010 && eyr <= 2030
        
        const hgt = passObj.get('hgt') || '0cm'
        const [hgtValue, hgtUnit] = [parseInt(hgt.substring(0,hgt.length-2)) || 0,hgt.substr(-2)]
        valid = valid && ['cm','in'].includes(hgtUnit)
        valid = valid && hgtUnit === 'cm'? hgtValue >= 150 && hgtValue <= 193 : hgtValue >= 59 && hgtValue <= 76
        
        const hcl = passObj.get('hcl') || '#'
        valid = valid && /^#[a-fA-F0-9]{6}$/.test(hcl) 
        
        const ecl = passObj.get('ecl') || '';
        valid = valid && ['amb','blu', 'brn', 'gry', 'grn', 'hzl', 'oth'].includes(ecl)
        
        const pid = passObj.get('pid') || ''
        valid = valid && /^[0-9]{9}$/.test(pid)
        
    }
    return valid
}

let result = passports.map(p => validate(p)).filter(it => it).length
console.log(result)
