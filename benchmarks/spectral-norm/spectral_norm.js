/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * spectral-norm benchmark in JavaScript
 */

'use strict';

function evalA(i, j) {
  return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1);
}

function evalATimesU(u, v) {
  const n = u.length;
  for (let i = 0; i < n; i++) {
    v[i] = 0;
    for (let j = 0; j < n; j++) {
      v[i] += evalA(i, j) * u[j];
    }
  }
}

function evalAtTimesU(u, v) {
  const n = u.length;
  for (let i = 0; i < n; i++) {
    v[i] = 0;
    for (let j = 0; j < n; j++) {
      v[i] += evalA(j, i) * u[j];
    }
  }
}

function evalAtATimesU(u, v, w) {
  evalATimesU(u, w);
  evalAtTimesU(w, v);
}

function main() {
  const n = process.argv.length > 2 ? parseInt(process.argv[2]) : 100;
  
  const u = new Array(n).fill(1.0);
  const v = new Array(n).fill(0.0);
  const w = new Array(n).fill(0.0);
  
  for (let i = 0; i < 10; i++) {
    evalAtATimesU(u, v, w);
    evalAtATimesU(v, u, w);
  }
  
  let vBv = 0.0;
  let vv = 0.0;
  
  for (let i = 0; i < n; i++) {
    vBv += u[i] * v[i];
    vv += v[i] * v[i];
  }
  
  console.log(Math.sqrt(vBv / vv).toFixed(9));
}

main();
