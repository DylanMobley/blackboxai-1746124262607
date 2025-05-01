#!/bin/bash

set -e

echo "🚀 Starting project setup..."

# Define paths
ENV_FILE=".env"
ENV_TEMPLATE=".env.template"
LOG_FILE="setup.log"
VENV_DIR=".venv"

# Step 1: Log file
mkdir -p logs
touch "logs/$LOG_FILE"

# Step 2: Python virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..." | tee -a "logs/$LOG_FILE"
    python3 -m venv "$VENV_DIR"
fi

echo "🧠 Activating virtualenv..." | tee -a "logs/$LOG_FILE"
source "$VENV_DIR/bin/activate"

# Step 3: Install dependencies
echo "📥 Installing Python packages..." | tee -a "logs/$LOG_FILE"
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Ensure .env exists
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_TEMPLATE" ]; then
        echo "🔧 Copying default .env file from template" | tee -a "logs/$LOG_FILE"
        cp "$ENV_TEMPLATE" "$ENV_FILE"
    else
        echo "⚠️ .env.template not found! Please create one." | tee -a "logs/$LOG_FILE"
    fi
else
    echo "✔️ .env file already exists" | tee -a "logs/$LOG_FILE"
fi

# Step 5: Run environment setup script
echo "🛠️ Running Python environment setup script..." | tee -a "logs/$LOG_FILE"
python scripts/init_environment.py >> "logs/$LOG_FILE" 2>&1

echo "✅ Setup complete." | tee -a "logs/$LOG_FILE"
