/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * regex-redux benchmark in JavaScript
 */

'use strict';

const fs = require('fs');

function main() {
  // Read input
  let input = '';
  const buffer = Buffer.alloc(65536);
  let bytesRead;
  
  while ((bytesRead = fs.readSync(0, buffer, 0, buffer.length)) > 0) {
    input += buffer.slice(0, bytesRead).toString('utf8');
  }
  
  // Remove header and newlines
  const sequence = input.replace(/>.*\n|\n/g, '');
  
  // Count patterns
  const initialLength = input.length;
  const codeLength = sequence.length;
  
  const patterns = [
    { regex: /agggtaaa|tttaccct/ig, name: 'agggtaaa|tttaccct' },
    { regex: /aggggtaaaa|tttacccct/ig, name: 'aggggtaaaa|tttacccct' },
    { regex: /agggggtaaaaa|tttaacccct/ig, name: 'agggggtaaaaa|tttaacccct' },
    { regex: /[cgt]gggtaaa|tttaccc[acg]/ig, name: '[cgt]gggtaaa|tttaccc[acg]' },
    { regex: /a[act]ggtaaa|tttacc[agt]t/ig, name: 'a[act]ggtaaa|tttacc[agt]t' },
    { regex: /ag[act]gtaaa|tttac[agt]ct/ig, name: 'ag[act]gtaaa|tttac[agt]ct' },
    { regex: /agg[act]taaa|ttta[agt]cct/ig, name: 'agg[act]taaa|ttta[agt]cct' },
    { regex: /aggg[acg]aaa|ttt[cgt]ccct/ig, name: 'aggg[acg]aaa|ttt[cgt]ccct' },
    { regex: /agggt[cgt]aa|tt[acg]accct/ig, name: 'agggt[cgt]aa|tt[acg]accct' },
    { regex: /agggta[cgt]a|t[acg]taccct/ig, name: 'agggta[cgt]a|t[acg]taccct' },
    { regex: /agggtaa[cgt]|[acg]ttaccct/ig, name: 'agggtaa[cgt]|[acg]ttaccct' }
  ];
  
  for (const pattern of patterns) {
    const matches = sequence.match(pattern.regex) || [];
    console.log(`${pattern.name} ${matches.length}`);
  }
  
  // Perform replacements
  let result = sequence;
  result = result.replace(/tHa[Nt]/g, '<4>');
  result = result.replace(/aND|caN|Ha[DS]|WaS/g, '<3>');
  result = result.replace(/a[NSt]|BY/g, '<2>');
  result = result.replace(/<[^>]*>/g, '|');
  result = result.replace(/\|[^|][^|]*\|/g, '-');
  
  console.log();
  console.log(initialLength);
  console.log(codeLength);
  console.log(result.length);
}

main();
