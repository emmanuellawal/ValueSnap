#!/bin/bash

# ValueSnap AI Image Generator Setup Script
# This script sets up the environment and runs tests

echo "🎨 ValueSnap AI Image Generator Setup"
echo "=" * 50

# Check if virtual environment exists in parent directory
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found. Please run from project root:"
    echo "   cd .."
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    exit 1
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source ../venv/bin/activate

# Install main requirements first
echo "📦 Installing main requirements..."
pip install -r ../requirements.txt

# Install AI-specific requirements
echo "📦 Installing AI image generation requirements..."
pip install -r requirements.txt

# Check if .env exists in parent directory
if [ ! -f "../.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example ../.env
    echo "📝 Please edit ../.env and add your OpenAI API key:"
    echo "   OPENAI_API_KEY=your_actual_api_key_here"
    echo ""
fi

# Run tests
echo "🧪 Running tests..."
python test_generate_ai_images.py

# Check if we have an API key to run the generator
if grep -q "your_openai_api_key_here" ../.env 2>/dev/null; then
    echo ""
    echo "⚠️  To generate actual images, update your ../.env file with a real OpenAI API key"
    echo "   Get one from: https://platform.openai.com/api-keys"
else
    echo ""
    echo "🚀 Ready to generate images! Run:"
    echo "   python generate_ai_images.py"
fi

echo ""
echo "✅ Setup complete!"