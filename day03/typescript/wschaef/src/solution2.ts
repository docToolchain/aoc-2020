import * as fs from 'fs';
import { TreeMap } from './TreeMap'
import { Trip } from './Trip'
const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n');

const map = new TreeMap(lines)
const trips = [
    new Trip(map).autoMove(1,1),
    new Trip(map).autoMove(3,1),
    new Trip(map).autoMove(5,1),
    new Trip(map).autoMove(7,1),
    new Trip(map).autoMove(1,2)
]
let result = trips.map(trip => trip.filter(value => value === "#").length).reduce((prod:number,elem) => prod * elem,1)
console.log(result)
