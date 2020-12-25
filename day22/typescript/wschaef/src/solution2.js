import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt', 'utf8');

const round = ([[x, ...xs], [y, ...ys]]) =>
    (x <= xs.length && y <= ys.length ? 
        play([xs.slice(0, x), ys.slice(0, y)]).winner == 0 : x > y) ? 
            [[...xs, x, y], ys] : [xs, [...ys, y, x]]

            const score = ([x, ...xs]) => x * (xs.length + 1) + (xs.length == 0 ? 0 : score(xs))

function play ([x, y], prev = new Set()){ (s =>
    prev.has(s) || y.length == 0 ? { winner: 0, score: score(x), deck: [x, y] } :
        x.length == 0 ? { winner: 1, score: score(y), deck: [x, y] } :
            play(round([x, y]), prev.add(s)))
    ([x, y].map(x => x.join("\n")).join("\n\n"))
}
    const result = play(input.trim().split("\n\n").map(x =>
    x.split("\n").slice(1).map(Number)))
console.log(result)
console.log(result.score)