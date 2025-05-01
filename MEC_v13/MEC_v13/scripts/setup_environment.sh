#!/bin/bash

# Setup script for MEC_v13 environment

echo "Updating package lists..."
sudo apt-get update

echo "Installing system dependencies..."
sudo apt-get install -y python3-pip python3-venv build-essential

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies from requirements.txt..."
pip install -r MEC_v13/requirements.txt

echo "Setting PYTHONPATH to include project root..."
export PYTHONPATH=$(pwd)/MEC_v13

echo "Environment setup complete. To activate the environment, run:"
echo "source venv/bin/activate"
echo "export PYTHONPATH=$(pwd)/MEC_v13"
