import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const numbers = input.split(',').map(it=> parseInt(it))

function tellNextNumber():number{
    let value = numbers[numbers.length-1]
    const lastIndex = numbers.slice(0,numbers.length-1).lastIndexOf(value)
    value = lastIndex > -1 ? numbers.length - lastIndex - 1 : 0
    numbers.push(value)
    return value
}
let value = 0
while(numbers.length < 2020){
    value = tellNextNumber()
}

const result = value
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
