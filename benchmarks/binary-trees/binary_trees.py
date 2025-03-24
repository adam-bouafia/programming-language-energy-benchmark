#!/usr/bin/env python3
"""
The Computer Language Benchmarks Game
https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

binary-trees benchmark in Python
"""

import sys
import multiprocessing


def make_tree(depth):
    if depth <= 0:
        return None, None, 0
    item = depth
    left = make_tree(depth - 1)
    right = make_tree(depth - 1)
    return left, right, item


def check_tree(node):
    left, right, item = node
    if left is None:
        return item
    return item + check_tree(left) - check_tree(right)


def make_check(depth, iterations):
    check = 0
    for i in range(iterations):
        tree = make_tree(depth)
        check += check_tree(tree)
    return check


def main(n, min_depth=4):
    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1

    print(f"stretch tree of depth {stretch_depth}\t check: {check_tree(make_tree(stretch_depth))}")

    long_lived_tree = make_tree(max_depth)

    mmd = max_depth + min_depth
    for depth in range(min_depth, max_depth + 1, 2):
        iterations = 2 ** (mmd - depth)
        check = make_check(depth, iterations)
        print(f"{iterations}\t trees of depth {depth}\t check: {check}")

    print(f"long lived tree of depth {max_depth}\t check: {check_tree(long_lived_tree)}")


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(n)
