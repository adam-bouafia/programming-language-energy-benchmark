# Repository Summary

This document provides a summary for testing programming language energy efficiency based on the paper "It's Not Easy Being Green: On the Energy Efficiency of Programming Languages".

## Repository Overview

The repository contains everything needed to run benchmarks that test the energy efficiency of different programming languages on your Kali Linux system with Intel Core i5 11th gen, 16GB RAM, and Intel Iris Xe graphics.

## Repository Structure

```
.
├── README.md                   # Main repository documentation
├── INSTALL.md                  # Installation instructions for Kali Linux
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore file
├── benchmarks/                 # Benchmark implementations
│   ├── binary-trees/           # Binary trees benchmark
│   │   ├── binary_trees.c
│   │   └── binary_trees.py
│   ├── mandelbrot/             # Mandelbrot set calculation
│   │   ├── mandelbrot.c
│   │   └── mandelbrot.py
│   ├── n-body/                 # N-body physics simulation
│   │   ├── n_body.c
│   │   └── n_body.py
│   ├── regex-redux/            # Regular expression benchmark
│   │   ├── regex_redux.c
│   │   └── regex_redux.py
│   └── spectral-norm/          # Spectral norm calculation
│       ├── spectral_norm.c
│       └── spectral_norm.py
├── scripts/                    # Measurement and utility scripts
│   ├── install_dependencies.sh # Script to install required dependencies
│   ├── measure_energy.py       # Script to measure energy consumption
│   └── run_benchmarks.sh       # Script to run all benchmarks
├── results/                    # Directory for benchmark results
└── docs/                       # Additional documentation
    ├── paper_summary.md        # Summary of the original paper
    └── measurement_methodology.md # Details on measurement methodology
```

## Key Components

1. **Benchmark Implementations**: 
   - 5 benchmarks from the Computer Language Benchmark Game (CLBG)
   - Each implemented in C and Python (expandable to other languages)

2. **Measurement Scripts**:
   - `install_dependencies.sh`: Installs all required programming languages and tools
   - `measure_energy.py`: Uses Intel RAPL to measure energy consumption
   - `run_benchmarks.sh`: Runs benchmarks and collects measurements

3. **Documentation**:
   - `README.md`: Overview of the repository
   - `INSTALL.md`: Step-by-step installation instructions
   - `docs/paper_summary.md`: Summary of the scientific paper
   - `docs/measurement_methodology.md`: Details on the measurement approach

## Getting Started

1. Clone the repository to your Kali Linux system
2. Follow the instructions in INSTALL.md
3. Run the benchmarks using the provided scripts
4. Analyze the results to compare energy efficiency across programming languages

## Expected Results

Based on the paper's findings, you should observe:
- A strong linear relationship between execution time and energy consumption
- Similar energy/time ratios across different programming languages for the same benchmark
- Performance differences primarily due to implementation details rather than language choice

This repository allows you to verify these findings on your own hardware and contribute to the understanding of programming language energy efficiency.
