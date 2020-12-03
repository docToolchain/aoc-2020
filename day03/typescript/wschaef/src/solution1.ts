import * as fs from 'fs';
import { TreeMap } from './TreeMap'
import { Trip } from './Trip'
const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n');

const map = new TreeMap(lines)
const trip = new Trip(map)
const points = trip.autoMove(3,1)

let result = points.filter(it => it === "#").length
console.log(result)
