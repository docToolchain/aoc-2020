import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

// const MIN_RESULT = 20000000000000 
const MIN_RESULT = 0

class Bus{
    constructor(public id:number,public offset:number){}
}

const busses = lines[1].split(',').map((bus,i)=>new Bus(parseInt(bus),i)).filter(bus => bus.id)

function getEaliestDeparture(id:number,minDepart:number):number{
    const a = minDepart/id
    if(a - Math.trunc(a) > 0) 
        return (Math.trunc(a) + 1) * id 
    else return minDepart
}

function checkRace(t:number,busList:Bus[]){
    const result = busList.every(bus => ((t+bus.offset)%bus.id === 0));
    return result
}
const firstBus= busses[0]
let t = getEaliestDeparture(firstBus.id,MIN_RESULT)
let step = firstBus.id
for(let i=2; i <= busses.length; i++) {
    const busList = busses.slice(0,i)
    while(!checkRace(t,busList) && (t < 10000000000000000000000)){
        t += step 
    }
    step = busList.reduce((prod,elem) => prod * elem.id, 1)
}
 
const result = t
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

