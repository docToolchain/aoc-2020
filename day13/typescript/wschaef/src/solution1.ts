import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
let lines = input.split('\n')

const myDepart = parseInt(lines[0])
const busses = lines[1].split(',').filter(it=>it !== 'x').map(it=> parseInt(it))

function getEaliestDeparture(id:number,minDepart:number):number{
    const a = minDepart/id
    if(Math.floor(a) > 0) 
        return Math.trunc(a) * id + id 
    else return Math.trunc(a) * id
}

const departures = busses.map(bus => [bus,getEaliestDeparture(bus, myDepart)]);
let [myBus,minDepart] = departures[0]
departures.forEach(([bus,departure]) => {
    if(departure < minDepart){
        minDepart = departure
        myBus = bus
    }
});

const result = (minDepart-myDepart) * myBus 
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  

