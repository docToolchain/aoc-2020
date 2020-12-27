import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n').map(l => l.slice(0,l.length-1).split(' (contains '))
                .map(([ingr,alerg]) => [ingr.split(' '),alerg.split(', ')])
const alergenAll = [...new Set(lines.map(([ingr,alerg]) => alerg).flat())]

function init(): string[][][] {
    return  alergenAll.map(alerg => [
        alerg,
        [...new Set(
            lines.filter(([ingr,a]) => a.includes(alerg)) // filter only lines with relevant alerg
            .map(([ingr,a]) => ingr)
            .reduce((a,b)=>a.filter(c => b.includes(c)))
        )] //get intersection
    ]) as string[][][]
} 

let alergens = init()

function reduce(input: string[][][], known:string[]){
    const result = input.map(([alerg,ingr]) => [alerg,ingr.filter(it => ingr.length == 1 || !known.includes(it))])
    return result
}

function solve(){
    const known = alergens.map(([alerg,ingr]) => ingr)
            .filter(ingr => ingr.length === 1).flat()
    if(known.length < alergens.length){
        alergens = reduce(alergens,known)
        solve()
    }
}
solve()
const ingredientsWithAlerg = alergens.map(([alerg,ingr]) => ingr).flat()
console.table(alergens)
const result = alergens.sort().map(it => it[1]).join()
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 