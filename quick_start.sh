#!/bin/bash

echo "🚀 Voice-to-Text Quick Start"
echo "============================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your Sarvam AI API key!"
    echo "   Open .env in your editor and replace 'your_sarvam_api_key_here' with your actual API key"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run setup test
echo "🧪 Running setup tests..."
python test_setup.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Run: python app.py"
echo "2. Open: http://localhost:8080"
echo "3. Enter PIN: 1234 (or your custom PIN)"
echo "4. Start recording or upload audio!"
echo ""
echo "For Docker deployment:"
echo "1. Run: docker-compose up --build"
echo "2. Open: http://localhost:8080"
