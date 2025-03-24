/**
 * The Computer Language Benchmarks Game
 * https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
 *
 * binary-trees benchmark in JavaScript
 */

'use strict';

class TreeNode {
  constructor(item, left = null, right = null) {
    this.item = item;
    this.left = left;
    this.right = right;
  }
}

function makeTree(depth) {
  if (depth <= 0) {
    return new TreeNode(0);
  }
  return new TreeNode(depth, makeTree(depth - 1), makeTree(depth - 1));
}

function checkTree(node) {
  if (node.left === null) {
    return node.item;
  }
  return node.item + checkTree(node.left) - checkTree(node.right);
}

function main() {
  const n = process.argv.length > 2 ? parseInt(process.argv[2]) : 10;
  const minDepth = 4;
  const maxDepth = Math.max(minDepth + 2, n);

  // Create and check stretch tree
  const stretchDepth = maxDepth + 1;
  const stretchTree = makeTree(stretchDepth);
  console.log(`stretch tree of depth ${stretchDepth}\t check: ${checkTree(stretchTree)}`);

  // Create long-lived tree
  const longLivedTree = makeTree(maxDepth);

  // Create, check, and delete multiple trees
  for (let depth = minDepth; depth <= maxDepth; depth += 2) {
    const iterations = 1 << (maxDepth - depth + minDepth);
    let check = 0;

    for (let i = 1; i <= iterations; i++) {
      const tempTree = makeTree(depth);
      check += checkTree(tempTree);
    }

    console.log(`${iterations}\t trees of depth ${depth}\t check: ${check}`);
  }

  // Check long-lived tree
  console.log(`long lived tree of depth ${maxDepth}\t check: ${checkTree(longLivedTree)}`);
}

main();
