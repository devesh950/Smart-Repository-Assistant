# Azure App Service startup script
#!/bin/bash

echo "🚀 Starting Smart Repository Assistant on Azure App Service..."

# Set up environment
export PYTHONPATH=/home/site/wwwroot
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8000

# Install requirements if not cached
if [ ! -f "/tmp/.requirements_installed" ]; then
    echo "📦 Installing Python requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch /tmp/.requirements_installed
    echo "✅ Requirements installed successfully"
fi

# Start the Flask application
echo "🌟 Starting Flask webhook server..."
cd /home/site/wwwroot
python app.py