import * as wasm from 'wasm-aoc';

import css from './index.css';

function runSolution(inputFileTxt) {
    const elemStar1Result = document.getElementById('star1-result');
    const elemStar2Result = document.getElementById('star2-result');
    const elemStar1Duration = document.getElementById('star1-duration');
    const elemStar2Duration = document.getElementById('star2-duration');

    if (inputFileTxt !== undefined) {
        const t0Star1 = performance.now();
        const resultStar1 = wasm.run_solution_star1(inputFileTxt);
        const t1Star1 = performance.now();
        elemStar1Result.innerText = resultStar1;
        elemStar1Duration.innerText = (t1Star1 - t0Star1).toFixed(2) + 'ms';

        const t0Star2 = performance.now();
        const resultStar2 = wasm.run_solution_star2(inputFileTxt);
        const t1Star2 = performance.now();
        elemStar2Result.innerText = resultStar2;
        elemStar2Duration.innerText = (t1Star2 - t0Star2).toFixed(2) + 'ms';
    } else {
        console.error('could not read input.txt file');
    }
}

function openFile(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function() {
        runSolution(reader.result);
    };
    reader.readAsText(input.files[0]);
};
window.openFile = openFile;