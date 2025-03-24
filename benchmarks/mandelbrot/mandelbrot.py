#!/usr/bin/env python3
"""
The Computer Language Benchmarks Game
https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

mandelbrot benchmark in Python
"""

import sys


def mandelbrot(size):
    result = bytearray()
    
    for y in range(size):
        bits = 0
        bit_num = 0
        
        for x in range(size):
            zr = zi = tr = ti = 0.0
            cr = (2.0 * x / size - 1.5)
            ci = (2.0 * y / size - 1.0)
            
            for i in range(50):
                zi = 2.0 * zr * zi + ci
                zr = tr - ti + cr
                tr = zr * zr
                ti = zi * zi
                
                if tr + ti > 4.0:
                    break
            
            bits = bits << 1 | (tr + ti <= 4.0)
            bit_num += 1
            
            if bit_num == 8:
                result.append(bits)
                bits = 0
                bit_num = 0
        
        if bit_num > 0:
            bits <<= (8 - bit_num)
            result.append(bits)
    
    return result


def main():
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    
    # Output PBM format header
    print(f"P4\n{size} {size}")
    
    # Calculate and output mandelbrot set
    sys.stdout.buffer.write(mandelbrot(size))


if __name__ == "__main__":
    main()
