import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
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
}
class Ticket{
    public fields: number[]
    constructor(private line:string){
        this.fields = line.split(',').map(it=>parseInt(it))
    }
    public getInvalidFields(rules: Rule[]):number[]{
        const result = this.fields.filter(f=>!this.isFieldValid(f,rules))
        return result
    }
    private isFieldValid(field:number, rules: Rule[]):boolean{
        const result = rules.some(r => r.ranges.some(([from, to]) => from <= field && field <= to));
        return result
    }
}
const rules = parsts[0].map(it=>new Rule(it))
const tickets = parsts[2].slice(1).map(it => new Ticket(it))

const result = tickets.map(t=> t.getInvalidFields(rules)).filter(it=>it).flat().reduce((sum,el)=> sum + el, 0)
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
