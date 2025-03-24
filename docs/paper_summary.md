# Paper Summary: "It's Not Easy Being Green: On the Energy Efficiency of Programming Languages"

## Authors
- Nicolas van Kempen, University of Massachusetts Amherst
- Hyuk-Je Kwon, University of Massachusetts Amherst
- Dung Tuan Nguyen, University of Massachusetts Amherst
- Emery D. Berger, University of Massachusetts Amherst / Amazon

## Overview
This paper challenges previous studies that claimed certain programming languages are inherently more energy efficient than others. The authors argue that these earlier studies established only associations between programming languages and energy consumption, but these associations have been misinterpreted as causal relationships in both academic and industrial contexts.

## Key Findings

1. **Energy Consumption is Primarily Related to Execution Time**
   - The paper demonstrates that energy consumption is directly proportional to runtime
   - When controlling for the number of active cores, the choice of programming language itself has no significant impact on energy consumption beyond its effect on execution time

2. **Critical Factors Affecting Energy Consumption**
   - Number of active cores
   - Memory activity
   - Application implementation specifics
   - Programming language implementation (not the language itself)

3. **Causal Model**
   - The paper develops a detailed causal model showing the relationship between programming language choice and energy consumption
   - This model identifies and incorporates several critical but previously overlooked factors that affect energy usage

4. **Methodological Improvements**
   - The authors correct technical errors in prior work that led to negative or incorrect energy readings
   - They present an improved methodology based on hardware performance counter data
   - They control for confounds like varying CPU utilization by forcing benchmarks to run on a single core

## Critique of Previous Studies

The paper identifies several flaws in previous studies:

1. **Programming Language vs. Implementation**
   - Previous studies failed to distinguish between programming languages and their implementations
   - Some languages have multiple implementations with different performance characteristics

2. **Quality of Benchmark Implementations**
   - Benchmark implementations have varied levels of parallelism, CPU usage, and use of third-party libraries
   - These differences are not properties of the languages themselves

3. **Unexplained Anomalies**
   - Previous studies reported counter-intuitive results without investigation or explanation
   - For example, C++ was reported as 34% less energy efficient than C, despite sharing the same compiler and backend

4. **Memory Metrics**
   - Previous studies used poor proxies for memory usage and activity
   - They did not account for cache activity, which significantly affects energy consumption

5. **Language Implementation Specifics**
   - Previous studies did not account for initial costs like JIT compilation warmup
   - They did not consider the impact of garbage collection on performance

## Conclusion

The paper concludes that to minimize energy consumption, programmers should focus primarily on optimizing performance rather than choosing a specific programming language. The choice of programming language implementation has no significant impact on energy consumption beyond execution time.

This repository allows you to test these findings on your own hardware by running benchmarks from the Computer Language Benchmark Game (CLBG) and measuring both execution time and energy consumption.
