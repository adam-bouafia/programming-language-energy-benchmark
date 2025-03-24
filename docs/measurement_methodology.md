# Measurement Methodology

This document describes the methodology used to measure energy consumption of programming languages in this repository, based on the approach outlined in the paper "It's Not Easy Being Green: On the Energy Efficiency of Programming Languages".

## Hardware Requirements

- Intel processor with RAPL support (Intel Core i5 11th gen or newer recommended)
- Linux-based operating system (tested on Kali Linux)
- 16GB RAM recommended

## Measurement Tools

### Intel RAPL (Running Average Power Limit)

Since the Sandy Bridge microarchitecture (2011), most Intel processors provide a power management interface called Running Average Power Limit (RAPL). This interface allows measurement of energy consumption of various parts of the system through Model Specific Registers (MSRs):

1. **MSR_RAPL_POWER_UNIT**: Contains information used to convert raw energy status counter values to joules
2. **MSR_PKG_ENERGY_STATUS**: Contains the raw energy status counter for the entire processor package
3. **MSR_DRAM_ENERGY_STATUS**: Contains the raw energy status counter for the RAM

Our measurement scripts access these registers to collect energy consumption data during benchmark execution.

### Performance Counters

Hardware performance counters track various events such as:
- Total CPU cycles
- Cache misses
- Branch misses

We use these counters to:
1. Estimate memory activity through Last Level Cache (LLC) misses
2. Track average CPU usage using the task-clock software event counter

## Measurement Process

Our measurement process follows these steps:

1. **Preparation**:
   - Reset performance counters
   - Read initial RAPL MSR values
   - Isolate benchmark execution to control for background processes

2. **During Execution**:
   - Continuously read RAPL MSRs at regular intervals (1Hz) to avoid counter overflow
   - Track performance counters

3. **After Execution**:
   - Read final performance counter values
   - Calculate total energy consumption
   - Calculate average core usage

## Controlling for Variables

To ensure fair comparison between programming languages, we control for several variables:

1. **Single-core Execution**:
   - Force benchmarks to run on a single core to eliminate the effect of varying concurrency
   - This is important because RAPL samples include all cores, even if the program only uses one

2. **Multiple Iterations**:
   - Run benchmarks multiple times to account for JIT compilation warmup
   - This is especially important for languages like Java and JavaScript

3. **Consistent Input Sizes**:
   - Use the same input parameters across all language implementations
   - This ensures we're comparing the same computational workload

4. **Isolation**:
   - Run benchmarks in isolated environments to minimize interference from other processes

## Data Collection

For each benchmark and language implementation, we collect:

1. **Execution Time**: Measured in seconds
2. **Energy Consumption**: Measured in joules
3. **Average Core Usage**: Calculated from task-clock counter
4. **Memory Activity**: Estimated from LLC misses

## Analysis

The primary analysis focuses on the relationship between execution time and energy consumption. According to the paper's findings, we expect to see:

1. A strong linear relationship between execution time and energy consumption
2. No significant difference in energy consumption between programming languages when normalized by execution time

The measurement scripts in this repository will generate CSV files with the collected data, allowing you to perform your own analysis and verify these findings on your hardware.

## Technical Considerations

- RAPL MSRs track energy consumption at the granularity of an entire package, not individual processes
- The measurement tool must be lightweight to minimize overhead
- RAPL counter overflow must be handled for long-running computations
- Proper conversion from raw counter values to joules is essential for accurate measurements
