#!/bin/bash
# chmod +x setup.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Print colored output
print_green() {
    echo -e "${GREEN}$1${NC}"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
fi

# Remove existing virtual environment if it exists
rm -rf imagegen_env

# Create virtual environment
print_green "Creating virtual environment..."
python3 -m venv imagegen_env

# Activate virtual environment
print_green "Activating virtual environment..."
source imagegen_env/bin/activate

# Upgrade pip
print_green "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_green "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_green "Installing dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please create one and run this script again."
    exit 1
fi

print_green "Setup complete! Activate the virtual environment with 'source venv/bin/activate'"