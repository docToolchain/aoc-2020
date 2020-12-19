import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const parsts = input.split('\n\n').map(it => it.split('\n'))

class Rule{
    public name: string
    public ranges: number[][]
    constructor(private ruleStr: string){
        const parts = ruleStr.split(': ')
        this.name = parts[0]
        this.ranges = parts[1].split(' or ').map(it=>it.split('-').map(it=>parseInt(it)))
    }
    public isFieldValid(field:number){
        return this.ranges.some(([from, to]) => from <= field && field <= to)
    }
}
class Ticket{
    public fields: number[]
    constructor(private line:string){
        this.fields = line.split(',').map(it=>parseInt(it))
    }
    public hasInvalidFields(rules: Rule[]):boolean{
        const result = this.fields.some(f=>!this.isFieldValid(f,rules))
        return result
    }
    private isFieldValid(field:number, rules: Rule[]):boolean{
        const result = rules.some(r => r.isFieldValid(field));
        return result
    }
}
const rules = parsts[0].map(it=>new Rule(it))
const myTicket = new Ticket(parsts[1][1])
const tickets = parsts[2].slice(1).map(it => new Ticket(it))
const validTickets = tickets.filter(t=>!t.hasInvalidFields(rules))
const positions = [...new Array(rules.length)].map((el,i)=>validTickets.map(t => t.fields[i])) 
const invalidRulesPerPositon = positions.map(p=>rules.filter(r=>p.some(value => !r.isFieldValid(value))).map(r=>r.name))
const validRulesPerPosition = invalidRulesPerPositon.map(ruleNames => rules.filter(r=>!ruleNames.includes(r.name)).map(r=>r.name))

function reduce(validRulesPerPosition: string[][]):string[][]{
    const fieldsWithOneValue = validRulesPerPosition.filter(p=>p.length === 1).flat()
    if(fieldsWithOneValue.length === validRulesPerPosition.length){
        return validRulesPerPosition
    }else{
        validRulesPerPosition = validRulesPerPosition.map(p=> p.length === 1 ? p : p.filter(ruleName => !fieldsWithOneValue.includes(ruleName)))
        return reduce(validRulesPerPosition)
    }
}

const fieldNamesPositions = reduce(validRulesPerPosition)
const result = fieldNamesPositions.map((name,i)=>[name[0],myTicket.fields[i].toString()])
                    .filter(([name,value])=> name.startsWith('departure '))
                    .reduce((p,[name,value])=> p * parseInt(value),1)

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
