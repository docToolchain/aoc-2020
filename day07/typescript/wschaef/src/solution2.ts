import * as fs from 'fs';

console.info("###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

const relationList = lines.map(line => line.split("contain "))
                    .map(it => [it[0],it[1].split(',')])

class Relation{
    constructor(
        public from: string,
        public to: string,
        public weight: number
    ){}
}

// e.g  [ 'shiny gold', 'dark red', '2' ],
function parseRelation(line: string):Relation[]{
    const from = line.split('contain ')[0]
                    .split(' ')
                    .slice(0,2)
                    .join(' ')
    const to = line.split('contain ')[1].split(', ')
                    .map(it => it.split(' '))
                    .map(it => it.slice(0,3))
                    .filter(it => it[0] !=='no')
    const relations = to.map(it=> new Relation(from, it.slice(1,3).join(' '),parseInt(it[0])))
    return relations
}
const relations = lines.map(line => parseRelation(line)).flat()

function countBagsInBag(bag: string) : number {
    const relevantRels = relations.filter(rel => rel.from === bag)
    const result = relevantRels.map(rel => rel.weight * countBagsInBag(rel.to)).reduce((sum,el) => sum+el,1)
    return result
}

const result = countBagsInBag('shiny gold') - 1 //remove 1 because shiny gold doesn't count itself

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  