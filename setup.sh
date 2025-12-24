#!/bin/bash
# Setup script for Smart Inverter Controller

echo "=================================="
echo "Smart Inverter Controller Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "=================================="
echo "✓ Setup completed successfully!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Get your Amber API token from: https://app.amber.com.au/settings/"
echo "2. Edit config.yaml with your details"
echo "3. Run: python3 test_amber_api.py"
echo "4. Run: python3 test_inverter.py"
echo "5. Run: python3 smart_controller.py --once"
echo ""
