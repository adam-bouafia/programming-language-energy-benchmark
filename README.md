# Programming Language Energy Efficiency Benchmark

This repository contains benchmarks for testing the energy efficiency of different programming languages, based on the scientific paper "It's Not Easy Being Green: On the Energy Efficiency of Programming Languages".

## Overview

The paper challenges previous studies that claimed certain programming languages (like Rust) are more energy efficient than others (like Python). The authors present a causal model showing that energy consumption is primarily related to execution time and the number of active cores, rather than the programming language itself.

This repository allows you to test this hypothesis on your own hardware by running benchmarks in multiple programming languages and measuring their energy consumption.

## Repository Structure

```
.
├── README.md                   # This file
├── benchmarks/                 # Benchmark implementations
│   ├── binary-trees/           # Binary trees benchmark
│   ├── mandelbrot/             # Mandelbrot set calculation
│   ├── n-body/                 # N-body physics simulation
│   ├── regex-redux/            # Regular expression benchmark
│   └── spectral-norm/          # Spectral norm calculation
├── scripts/                    # Measurement and utility scripts
│   ├── install_dependencies.sh # Script to install required dependencies
│   ├── measure_energy.py       # Script to measure energy consumption
│   └── run_benchmarks.sh       # Script to run all benchmarks
├── results/                    # Directory for benchmark results
└── docs/                       # Additional documentation
    ├── paper_summary.md        # Summary of the original paper
    └── measurement_methodology.md # Details on measurement methodology
```


## Supported Languages

- C
- Python
- Java
- JavaScript (Node.js)
- Rust

## Benchmarks

The benchmarks are selected from the Computer Language Benchmark Game (CLBG):

1. **binary-trees** - Tests memory allocation/deallocation performance
2. **mandelbrot** - Computationally intensive, tests CPU performance
3. **n-body** - Physics simulation, tests floating-point performance
4. **regex-redux** - Tests regular expression performance
5. **spectral-norm** - Mathematical computation benchmark

## Requirements

- Linux system with Intel processor (RAPL support required for energy measurements)
- Kali Linux recommended (tested on Kali with Intel Core i5 11th gen, 16GB RAM)
- Root access (for energy measurements)

## Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

Quick start:
```bash
# Install dependencies
./scripts/install_dependencies.sh

# Run benchmarks
./scripts/run_benchmarks.sh
```

## Measurement Methodology

The energy measurements are performed using Intel's Running Average Power Limit (RAPL) interface, which provides accurate energy consumption data for Intel processors. The methodology is described in detail in [docs/measurement_methodology.md](docs/measurement_methodology.md).

## Paper Summary

For a summary of the original scientific paper and its findings, see [docs/paper_summary.md](docs/paper_summary.md).

## Results

After running the benchmarks, results will be saved in the `results/` directory in both CSV and JSON formats. The script will also display a summary of the results in the terminal.

The key metric to observe is the Energy/Time ratio. According to the paper, if energy consumption is primarily related to execution time rather than language choice, this ratio should be similar across different programming languages for the same benchmark.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to add more language implementations, improve the measurement methodology, or enhance the documentation.

## Acknowledgments

- The original paper authors for their research on programming language energy efficiency
- The Computer Language Benchmark Game for providing the benchmark implementations
