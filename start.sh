#!/bin/bash

# Smart Repository Assistant - Linux/macOS Startup Script

echo "Smart Repository Assistant - Unix Startup Script"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Run setup if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Running initial setup..."
    python setup.py
    if [ $? -ne 0 ]; then
        echo "Error: Setup failed"
        exit 1
    fi
fi

# Run system test
echo "Running system test..."
python test_system.py
if [ $? -ne 0 ]; then
    echo "Warning: System test found issues"
    echo "Please check your configuration"
    read -p "Press Enter to continue..."
fi

echo ""
echo "=================================================="
echo "Choose what to start:"
echo "1. Webhook Server (Flask App)"
echo "2. Analytics Dashboard (Streamlit)"
echo "3. Both (in background)"
echo "4. Exit"
echo "=================================================="
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Starting webhook server..."
        python app.py
        ;;
    2)
        echo "Starting analytics dashboard..."
        streamlit run dashboard.py
        ;;
    3)
        echo "Starting both services..."
        python app.py &
        FLASK_PID=$!
        echo "Flask server started with PID: $FLASK_PID"
        
        streamlit run dashboard.py &
        STREAMLIT_PID=$!
        echo "Streamlit dashboard started with PID: $STREAMLIT_PID"
        
        echo "Both services started. Press Ctrl+C to stop."
        trap "kill $FLASK_PID $STREAMLIT_PID" EXIT
        wait
        ;;
    4)
        echo "Goodbye!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac