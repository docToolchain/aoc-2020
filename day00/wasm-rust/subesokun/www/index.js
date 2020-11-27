import * as wasm from 'wasm-aoc';

import inputFileTxt from '../input.txt';

if (inputFileTxt !== undefined) {
    wasm.run_solution(inputFileTxt);
} else {
    console.error('could not read input.txt file');
}
