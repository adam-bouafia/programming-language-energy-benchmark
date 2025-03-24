#!/bin/bash
# install_dependencies.sh - Script to install required dependencies for programming language energy efficiency benchmarks

set -e  # Exit on error

echo "Installing dependencies for Programming Language Energy Efficiency Benchmark..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install basic build tools
echo "Installing build tools..."
sudo apt-get install -y build-essential cmake git

# Install bc for calculations
echo "Installing bc..."
sudo apt-get install bc  

# Install C/C++ compilers and libraries
echo "Installing C/C++ tools..."
sudo apt-get install -y gcc g++ clang libpcre3-dev

# Install Python and PyPy
echo "Installing Python..."
sudo apt-get install -y python3 python3-pip python3-dev pypy3

# Install Node.js (for JavaScript)
if ! command_exists node; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "Node.js already installed."
fi

# Install Java
echo "Installing Java..."
sudo apt-get install -y default-jdk

# Install Rust
if ! command_exists rustc; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust already installed."
fi

# Install tools for energy measurement
echo "Installing energy measurement tools..."
sudo apt-get install -y linux-tools-common linux-tools-generic

# Install Python packages for measurement
echo "Installing Python packages for measurement..."
pip3 install numpy pandas matplotlib psutil

# Install bc for calculations
echo "Installing bc for calculations..."
sudo apt-get install -y bc

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

echo "Installation complete!"
echo "You can now run the benchmarks using ./scripts/run_benchmarks.sh"
