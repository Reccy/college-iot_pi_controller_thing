#!/usr/bin/env bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Introduction
echo "RaspberryPi / GrovePi Configuration Program"
echo "By Aaron Meaney - 2018"
echo ""

# Check if the project is in a good state to be ran
echo "Running self-check..."

# Check if running on a Raspberry Pi
echo "Checking if running on a Raspberry Pi"
if cat /proc/device-tree/model | grep "Raspberry Pi"; then
	echo "OK: Running on a Raspberry Pi"
else
	echo "ERROR: Not Running on Raspberry Pi! Please run this program on a Raspberry Pi"
	exit 1
fi

# Check if Python version is correct
echo "Checking if Python is installed"
if command -v python &>/dev/null; then
    echo "OK: Python is installed"
else
    echo "ERROR: Python is not installed. Please install Python to run this program"
    exit 1
fi

# Run the Python script
echo "Self-check Complete"
echo "Starting application..."
echo ""
python $DIR/bin/pi_controller.py