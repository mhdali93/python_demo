#!/bin/bash

# Database Connection Pooling Demo Runner
echo "===== Database Connection Pooling Demo ====="

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the comparison
echo "Running performance comparison..."
python compare_performance.py

# Display final message
echo ""
echo "Demo complete!"
echo "Results summary is shown above."
if [ -f "performance_comparison.png" ]; then
    echo "Performance chart saved as: $(pwd)/performance_comparison.png"
fi

# Deactivate virtual environment
deactivate 