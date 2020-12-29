import * as fs from 'fs';
import { isMainThread } from 'worker_threads';
import { log } from 'util';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n').map(it=>parseInt(it))

const [dPublicKey,rPublicKey] = lines

function transform(x:number,s:number){
    return (x * s) % 20201227
}

function calcLoops(publicKey:number){
    let state = 1
    let i = 0
    while (state !== publicKey) {
        i++
        state = transform(state,7)
    }
    return i
}

function calcEncryptionKey(loops:number,publicKey:number){
    let result = 1
    for(let i=0; i<loops; i++){
        result = transform(result,publicKey)
    }
    return result
}

const result = calcEncryptionKey(calcLoops(rPublicKey),dPublicKey)
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 