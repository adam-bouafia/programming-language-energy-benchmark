/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * mandelbrot benchmark in JavaScript
 */

'use strict';

function mandelbrot(size) {
  const result = new Uint8Array(Math.ceil(size / 8) * size);
  let dataIndex = 0;
  
  for (let y = 0; y < size; y++) {
    let bitIndex = 0;
    let byteAcc = 0;
    
    for (let x = 0; x < size; x++) {
      let zr = 0;
      let zi = 0;
      const cr = (2.0 * x / size - 1.5);
      const ci = (2.0 * y / size - 1.0);
      let tr = 0;
      let ti = 0;
      let i = 0;
      
      for (i = 0; i < 50 && tr + ti <= 4.0; i++) {
        zi = 2.0 * zr * zi + ci;
        zr = tr - ti + cr;
        tr = zr * zr;
        ti = zi * zi;
      }
      
      byteAcc <<= 1;
      if (tr + ti <= 4.0) {
        byteAcc |= 1;
      }
      
      bitIndex++;
      
      if (bitIndex === 8) {
        result[dataIndex++] = byteAcc;
        byteAcc = 0;
        bitIndex = 0;
      } else if (x === size - 1) {
        byteAcc <<= (8 - bitIndex);
        result[dataIndex++] = byteAcc;
        byteAcc = 0;
        bitIndex = 0;
      }
    }
  }
  
  return result;
}

function main() {
  const size = process.argv.length > 2 ? parseInt(process.argv[2]) : 200;
  
  process.stdout.write(`P4\n${size} ${size}\n`);
  
  const data = mandelbrot(size);
  process.stdout.write(Buffer.from(data));
}

main();
