#!/usr/bin/env python3
"""
measure_energy.py - Script to measure energy consumption of programming language benchmarks
using Intel RAPL interface and performance counters.
"""

import os
import sys
import time
import subprocess
import argparse
import csv
import json
from datetime import datetime
import numpy as np

# Constants
MSR_RAPL_POWER_UNIT = 0x606
MSR_PKG_ENERGY_STATUS = 0x611
MSR_DRAM_ENERGY_STATUS = 0x619
ENERGY_UNIT_MASK = 0x1F00
ENERGY_UNIT_OFFSET = 8

class EnergyMeasurement:
    def __init__(self, cpu=0, sample_rate=1.0):
        self.cpu = cpu
        self.sample_rate = sample_rate
        self.msr_file = f"/dev/cpu/{cpu}/msr"
        self.samples = []
        self.energy_unit = None
        self.start_time = None
        self.end_time = None
        self.total_energy = 0.0
        self.pkg_before = None
        self.dram_before = None
        
        # Check if MSR is accessible
        if not os.path.exists(self.msr_file):
            print(f"Error: MSR file {self.msr_file} does not exist.")
            print("Make sure the msr module is loaded (sudo modprobe msr)")
            print("and you have read permissions (sudo chmod +r /dev/cpu/*/msr)")
            sys.exit(1)
        
        # Get energy unit
        self._get_energy_unit()
    
    def _read_msr(self, register):
        """Read a value from MSR."""
        try:
            with open(self.msr_file, 'rb') as f:
                f.seek(register)
                value = int.from_bytes(f.read(8), byteorder='little')
                return value
        except Exception as e:
            print(f"Error reading MSR: {e}")
            sys.exit(1)
    
    def _get_energy_unit(self):
        """Get the energy unit from RAPL power unit register."""
        rapl_power_unit = self._read_msr(MSR_RAPL_POWER_UNIT)
        energy_unit_val = (rapl_power_unit & ENERGY_UNIT_MASK) >> ENERGY_UNIT_OFFSET
        self.energy_unit = 0.5 ** energy_unit_val
        print(f"Energy unit: {self.energy_unit} joules")
    
    def _get_energy(self):
        """Get current energy consumption."""
        pkg_energy = self._read_msr(MSR_PKG_ENERGY_STATUS) & 0xFFFFFFFF  # Use only lower 32 bits
        dram_energy = self._read_msr(MSR_DRAM_ENERGY_STATUS) & 0xFFFFFFFF
        return pkg_energy, dram_energy
    
    def start(self):
        """Start energy measurement."""
        self.start_time = time.time()
        self.pkg_before, self.dram_before = self._get_energy()
        self.samples = []
        return self
    
    def sample(self):
        """Take an energy sample."""
        pkg_now, dram_now = self._get_energy()
        
        # Handle counter overflow
        if pkg_now < self.pkg_before:
            pkg_energy = (0xFFFFFFFF - self.pkg_before + pkg_now) * self.energy_unit
        else:
            pkg_energy = (pkg_now - self.pkg_before) * self.energy_unit
            
        if dram_now < self.dram_before:
            dram_energy = (0xFFFFFFFF - self.dram_before + dram_now) * self.energy_unit
        else:
            dram_energy = (dram_now - self.dram_before) * self.energy_unit
        
        self.samples.append((pkg_energy, dram_energy))
        self.pkg_before, self.dram_before = pkg_now, dram_now
    
    def stop(self):
        """Stop energy measurement and calculate total energy."""
        self.end_time = time.time()
        self.sample()  # Take final sample
        
        # Calculate total energy
        pkg_total = sum(sample[0] for sample in self.samples)
        dram_total = sum(sample[1] for sample in self.samples)
        self.total_energy = pkg_total + dram_total
        
        return {
            'duration': self.end_time - self.start_time,
            'pkg_energy': pkg_total,
            'dram_energy': dram_total,
            'total_energy': self.total_energy
        }
    
    def monitor_process(self, command, shell=False):
        """Monitor energy consumption of a process."""
        print(f"Running command: {command}")
        
        # Start measurement
        self.start()
        
        # Start process
        start_time = time.time()
        process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Sample energy while process is running
        while process.poll() is None:
            self.sample()
            time.sleep(1.0 / self.sample_rate)
        
        # Get process output
        stdout, stderr = process.communicate()
        end_time = time.time()
        
        # Stop measurement
        result = self.stop()
        
        # Add process info to result
        result['command'] = command
        result['return_code'] = process.returncode
        result['stdout'] = stdout.decode('utf-8', errors='replace')
        result['stderr'] = stderr.decode('utf-8', errors='replace')
        
        return result

def run_benchmark(benchmark, language, params="", iterations=3):
    """Run a benchmark in a specific language and measure energy consumption."""
    results = []
    
    # Determine command based on language
    if language == "c":
        cmd = f"cd /home/ubuntu/benchmarks/{benchmark} && gcc -O3 -o {benchmark} {benchmark}.c && ./{benchmark} {params}"
    elif language == "python":
        cmd = f"cd /home/ubuntu/benchmarks/{benchmark} && python3 {benchmark}.py {params}"
    elif language == "javascript":
        cmd = f"cd /home/ubuntu/benchmarks/{benchmark} && node {benchmark}.js {params}"
    elif language == "java":
        # Java uses CamelCase for class names
        class_name = ''.join(word.capitalize() for word in benchmark.split('-'))
        cmd = f"cd /home/ubuntu/benchmarks/{benchmark} && javac {class_name}.java && java {class_name} {params}"
    elif language == "rust":
        cmd = f"cd /home/ubuntu/benchmarks/{benchmark} && rustc -O {benchmark}.rs && ./{benchmark} {params}"
    else:
        print(f"Unsupported language: {language}")
        return None
    
    # Run benchmark multiple times
    for i in range(iterations):
        print(f"Running {benchmark} in {language}, iteration {i+1}/{iterations}")
        measurement = EnergyMeasurement()
        result = measurement.monitor_process(cmd, shell=True)
        results.append(result)
        time.sleep(1)  # Short pause between iterations
    
    # Calculate average results
    avg_result = {
        'benchmark': benchmark,
        'language': language,
        'params': params,
        'iterations': iterations,
        'avg_duration': np.mean([r['duration'] for r in results]),
        'avg_pkg_energy': np.mean([r['pkg_energy'] for r in results]),
        'avg_dram_energy': np.mean([r['dram_energy'] for r in results]),
        'avg_total_energy': np.mean([r['total_energy'] for r in results]),
        'std_duration': np.std([r['duration'] for r in results]),
        'std_total_energy': np.std([r['total_energy'] for r in results]),
        'timestamp': datetime.now().isoformat()
    }
    
    return avg_result

def save_results(results, output_dir="/home/ubuntu/results"):
    """Save benchmark results to CSV and JSON files."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"benchmark_results_{timestamp}.csv")
    json_file = os.path.join(output_dir, f"benchmark_results_{timestamp}.json")
    
    # Save as CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    # Save as JSON
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {csv_file} and {json_file}")
    return csv_file, json_file

def main():
    parser = argparse.ArgumentParser(description='Measure energy consumption of programming language benchmarks')
    parser.add_argument('--benchmark', type=str, help='Specific benchmark to run')
    parser.add_argument('--language', type=str, help='Specific language to run')
    parser.add_argument('--params', type=str, default="", help='Parameters to pass to the benchmark')
    parser.add_argument('--iterations', type=int, default=3, help='Number of iterations to run')
    parser.add_argument('--output', type=str, default="/home/ubuntu/results", help='Output directory for results')
    
    args = parser.parse_args()
    
    # Define available benchmarks and languages
    benchmarks = ["binary-trees", "mandelbrot", "n-body", "regex-redux", "spectral-norm"]
    languages = ["c", "python", "javascript", "java", "rust"]  # Added more languages
    
    # Filter based on arguments
    if args.benchmark:
        if args.benchmark not in benchmarks:
            print(f"Error: Benchmark {args.benchmark} not found. Available benchmarks: {benchmarks}")
            sys.exit(1)
        benchmarks = [args.benchmark]
    
    if args.language:
        if args.language not in languages:
            print(f"Error: Language {args.language} not supported. Available languages: {languages}")
            sys.exit(1)
        languages = [args.language]
    
    # Run benchmarks
    results = []
    for benchmark in benchmarks:
        for language in languages:
            result = run_benchmark(benchmark, language, args.params, args.iterations)
            if result:
                results.append(result)
                print(f"Results for {benchmark} in {language}:")
                print(f"  Duration: {result['avg_duration']:.4f} seconds (±{result['std_duration']:.4f})")
                print(f"  Energy: {result['avg_total_energy']:.4f} joules (±{result['std_total_energy']:.4f})")
                print()
    
    # Save results
    if results:
        save_results(results, args.output)

if __name__ == "__main__":
    main()
