#!/bin/bash

# Exit on error
set -e

# Navigate to app directory
cd "$(dirname "$0")"
echo "Working directory: $(pwd)"

# Check Python version
python_version=$(python3 --version)
echo "Using $python_version"

# Activate virtual environment (create it if it doesn't exist)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Verify we're using the virtual environment python
which python
which pip

# Install or update dependencies with verbose output
echo "Installing dependencies..."
pip install --verbose -r requirements.txt

# Verify FastAPI is installed
echo "Checking if FastAPI is installed..."
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

# Check for common issues
echo "Checking for potential issues..."
if [ ! -d "templates" ]; then
    echo "WARNING: templates directory not found, creating it..."
    mkdir -p templates
fi

if [ ! -d "static" ]; then
    echo "WARNING: static directory not found, creating it..."
    mkdir -p static
fi

# Start the application with the venv Python
echo "Starting FastAPI application..."
echo "Access the application at http://$(hostname -I | awk '{print $1}'):8000"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
