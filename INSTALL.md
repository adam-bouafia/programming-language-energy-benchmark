# Installation Instructions for Kali Linux

This document provides step-by-step instructions for setting up and running the Programming Language Energy Efficiency Benchmark and tested on my Kali Linux system with Intel Core i5 11th gen, 16GB RAM, and Intel Iris Xe graphics.

## Prerequisites

- Linux installed on your system
- Internet connection
- Administrator (sudo) privileges
- Intel Core i5 11th gen processor (or other Intel processor with RAPL support)
- 16GB RAM

## Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/adam-bouafia/programming-language-energy-benchmark.git
cd programming-language-energy-benchmark
```

## Step 2: Install Dependencies

Run the installation script to install all necessary dependencies:

```bash
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

This script will install:
- C/C++ compilers (GCC, Clang)
- Python (CPython and PyPy)
- Node.js (JavaScript)
- Java (OpenJDK)
- Rust (via rustup)
- Required measurement tools

The script requires sudo privileges to install packages and set up the necessary permissions for energy measurement.

## Step 3: Make Scripts Executable

Ensure all scripts are executable:

```bash
chmod +x scripts/run_benchmarks.sh
chmod +x scripts/measure_energy.py
```

## Step 4: Run Benchmarks

You can run all benchmarks with the default settings:

```bash
./scripts/run_benchmarks.sh
```

Or run specific benchmarks and languages:

```bash
# Run mandelbrot benchmark in C
./scripts/run_benchmarks.sh -b mandelbrot -l c

# Run binary-trees benchmark with parameter 10
./scripts/run_benchmarks.sh -b binary-trees -p 10

# Run all benchmarks with 5 iterations
./scripts/run_benchmarks.sh -i 5
```

## Step 5: View Results

After running the benchmarks, results will be saved in the `results/` directory in both CSV and JSON formats. The script will also display a summary of the results in the terminal.

To view the results later:

```bash
# List all result files
ls -l results/

# View the latest CSV result file
cat $(ls -t results/*.csv | head -1)
```

## Troubleshooting

### MSR Access Issues

If you encounter permission issues with MSR access, try:

```bash
sudo modprobe msr
sudo chmod +r /dev/cpu/*/msr
```

### Benchmark Compilation Errors

If you encounter compilation errors for specific benchmarks:

1. Check that all dependencies were installed correctly
2. Try running the specific benchmark manually:
   ```bash
   cd benchmarks/benchmark-name
   gcc -O3 -o benchmark_name benchmark_name.c
   ./benchmark_name
   ```

### Energy Measurement Not Working

If energy measurement isn't working:

1. Verify your processor supports RAPL:
   ```bash
   grep -q "intel_rapl" /proc/modules && echo "RAPL supported" || echo "RAPL not supported"
   ```

2. Check if MSR is accessible:
   ```bash
   ls -l /dev/cpu/0/msr
   ```

## Additional Options

For more options and detailed usage information:

```bash
./scripts/run_benchmarks.sh --help
python3 scripts/measure_energy.py --help
```

## Understanding the Results

The benchmark results include:

- **Duration**: Execution time in seconds
- **Energy**: Total energy consumption in joules
- **Energy/Time Ratio**: Energy consumption divided by execution time

According to the paper, if energy consumption is primarily related to execution time rather than language choice, the Energy/Time ratio should be similar across different programming languages for the same benchmark.
