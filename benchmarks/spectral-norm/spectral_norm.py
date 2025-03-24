#!/usr/bin/env python3
"""
The Computer Language Benchmarks Game
https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

spectral-norm benchmark in Python
"""

import sys
import math

def eval_A(i, j):
    return 1.0 / ((i + j) * (i + j + 1) // 2 + i + 1)

def eval_A_times_u(u, Au):
    n = len(u)
    for i in range(n):
        Au[i] = 0
        for j in range(n):
            Au[i] += eval_A(i, j) * u[j]

def eval_At_times_u(u, Au):
    n = len(u)
    for i in range(n):
        Au[i] = 0
        for j in range(n):
            Au[i] += eval_A(j, i) * u[j]

def eval_AtA_times_u(u, AtAu):
    n = len(u)
    v = [0] * n
    eval_A_times_u(u, v)
    eval_At_times_u(v, AtAu)

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    u = [1.0] * n
    v = [0.0] * n
    
    for i in range(10):
        eval_AtA_times_u(u, v)
        eval_AtA_times_u(v, u)
    
    vBv = vv = 0
    for i in range(n):
        vBv += u[i] * v[i]
        vv += v[i] * v[i]
    
    print(f"{math.sqrt(vBv / vv):.9f}")

if __name__ == "__main__":
    main()
