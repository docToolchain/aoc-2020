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
        public count: number
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
// console.log(relations)

function listBagsContainsBag(bag: string, resultSet: Set<string>, fromBag: string = '') : boolean {
    let result = false
    const rels = (fromBag === '')?relations:relations.filter(rel => rel.from === fromBag)
    rels.forEach(relation => {
        if(resultSet.has(relation.from)){
            result = true
        }
        else{
            if(bag === relation.to) {
                resultSet.add(relation.from)
                result = true
            }
            if(listBagsContainsBag(bag,resultSet,relation.to)){
                resultSet.add(relation.from)
                result = true
            }
        }
    })
    return result
}

let resultSet = new Set<string>();
listBagsContainsBag('shiny gold', resultSet)

const result = resultSet.size

console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  