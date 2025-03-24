#!/usr/bin/env python3
"""
The Computer Language Benchmarks Game
https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

regex-redux benchmark in Python
"""

import re
import sys


def main():
    # Read input file or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            sequence = f.read()
    else:
        sequence = sys.stdin.read()
    
    # Skip initial description
    sequence = sequence[sequence.find('>THREE'):].split('\n', 1)[1]
    
    # Remove newlines
    sequence = re.sub(r'\n', '', sequence)
    initial_length = len(sequence)
    
    # Count pattern matches
    variants = [
        r'agggtaaa|tttaccct',
        r'[cgt]gggtaaa|tttaccc[acg]',
        r'a[act]ggtaaa|tttacc[agt]t',
        r'ag[act]gtaaa|tttac[agt]ct',
        r'agg[act]taaa|ttta[agt]cct',
        r'aggg[acg]aaa|ttt[cgt]ccct',
        r'agggt[cgt]aa|tt[acg]accct',
        r'agggta[cgt]a|t[acg]taccct',
        r'agggtaa[cgt]|[acg]ttaccct'
    ]
    
    for variant in variants:
        count = len(re.findall(variant, sequence))
        print(f"{variant} {count}")
    
    # Perform substitutions
    substitutions = [
        (r'tHa[Nt]', '<4>'),
        (r'aND|cAN|Ha[DS]|WaS', '<3>'),
        (r'a[NSt]|BY', '<2>'),
        (r'<[^>]*>', '|'),
        (r'\|[^|][^|]*\|', '-')
    ]
    
    for pattern, replacement in substitutions:
        sequence = re.sub(pattern, replacement, sequence)
    
    print(f"\nLength before: {initial_length}")
    print(f"Length after: {len(sequence)}")


if __name__ == "__main__":
    main()
