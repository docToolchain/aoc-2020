import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const numbers = input.split(',').map(it=> parseInt(it))
let lookup = numbers.slice(0,numbers.length-1).reduce((map,n) => map.set(n,numbers.lastIndexOf(n)), new Map<number,number>())

function tellNextNumber():number{
    let value = numbers[numbers.length-1]
    const lastIndex = lookup.get(value) ?? -1
    lookup.set(value,numbers.length-1)
    value = lastIndex > -1 ? numbers.length - lastIndex - 1 : 0
    numbers.push(value)
    return value
}
let value = 0
console.time()
while(numbers.length < 30000000){
    value = tellNextNumber()
}
console.timeEnd()

const result = value
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
