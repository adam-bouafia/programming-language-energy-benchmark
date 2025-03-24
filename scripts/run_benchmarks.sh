#!/bin/bash
# run_benchmarks.sh - Script to run programming language energy efficiency benchmarks

set -e  # Exit on error

# Default values
BENCHMARK=""
LANGUAGE=""
PARAMS=""
ITERATIONS=3
OUTPUT_DIR="/home/ubuntu/results"

# Function to display usage information
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -b, --benchmark BENCHMARK  Specific benchmark to run (binary-trees, mandelbrot, n-body, regex-redux, spectral-norm)"
    echo "  -l, --language LANGUAGE    Specific language to run (c, python, javascript, java, rust)"
    echo "  -p, --params PARAMS        Parameters to pass to the benchmark"
    echo "  -i, --iterations N         Number of iterations to run (default: 3)"
    echo "  -o, --output DIR           Output directory for results (default: /home/ubuntu/results)"
    echo "  -h, --help                 Display this help message"
    echo
    echo "Examples:"
    echo "  $0                         # Run all benchmarks in all languages"
    echo "  $0 -b mandelbrot -l c      # Run mandelbrot benchmark in C"
    echo "  $0 -b binary-trees -p 10   # Run binary-trees benchmark with parameter 10"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--benchmark)
            BENCHMARK="$2"
            shift 2
            ;;
        -l|--language)
            LANGUAGE="$2"
            shift 2
            ;;
        -p|--params)
            PARAMS="$2"
            shift 2
            ;;
        -i|--iterations)
            ITERATIONS="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if measure_energy.py exists
if [ ! -f "$(dirname "$0")/measure_energy.py" ]; then
    echo "Error: measure_energy.py not found in the same directory as this script."
    exit 1
fi

# Check if MSR module is loaded
if ! lsmod | grep msr > /dev/null; then
    echo "Loading MSR module..."
    sudo modprobe msr
fi

# Check if user has access to MSR
if [ ! -r /dev/cpu/0/msr ]; then
    echo "Setting permissions for MSR access..."
    sudo chmod +r /dev/cpu/0/msr
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run benchmarks
echo "Running benchmarks..."
echo "--------------------"

# Construct command arguments
CMD_ARGS=""
if [ -n "$BENCHMARK" ]; then
    CMD_ARGS="$CMD_ARGS --benchmark $BENCHMARK"
fi
if [ -n "$LANGUAGE" ]; then
    CMD_ARGS="$CMD_ARGS --language $LANGUAGE"
fi
if [ -n "$PARAMS" ]; then
    CMD_ARGS="$CMD_ARGS --params $PARAMS"
fi
CMD_ARGS="$CMD_ARGS --iterations $ITERATIONS --output $OUTPUT_DIR"

# Run the Python measurement script
python3 "$(dirname "$0")/measure_energy.py" $CMD_ARGS

echo "--------------------"
echo "Benchmarks completed. Results saved to $OUTPUT_DIR"

# Generate a simple report
LATEST_CSV=$(ls -t "$OUTPUT_DIR"/*.csv | head -1)
if [ -n "$LATEST_CSV" ]; then
    echo
    echo "Summary of results:"
    echo "------------------"
    echo "Benchmark | Language | Duration (s) | Energy (J) | Energy/Time Ratio"
    echo "----------|----------|--------------|------------|------------------"
    
    # Skip header and process each line
    tail -n +2 "$LATEST_CSV" | while IFS=, read -r line; do
        # Extract fields (this is a simplified version, actual CSV parsing would be more robust)
        benchmark=$(echo "$line" | cut -d, -f1)
        language=$(echo "$line" | cut -d, -f2)
        duration=$(echo "$line" | cut -d, -f5)
        energy=$(echo "$line" | cut -d, -f8)
        
        # Calculate energy/time ratio
        ratio=$(echo "scale=4; $energy / $duration" | bc)
        
        # Format and print the line
        printf "%-10s | %-8s | %12.4f | %10.4f | %18.4f\n" "$benchmark" "$language" "$duration" "$energy" "$ratio"
    done
    
    echo
    echo "Note: According to the paper, the energy/time ratio should be similar across languages"
    echo "if energy consumption is primarily related to execution time rather than language choice."
fi
