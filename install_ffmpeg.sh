#!/bin/bash

echo "🎬 Installing FFmpeg for Voice-to-Text App"
echo "=========================================="

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 Detected macOS"
    
    # Try to install via Homebrew
    if command -v brew &> /dev/null; then
        echo "🍺 Homebrew found, installing FFmpeg..."
        brew install ffmpeg
    else
        echo "❌ Homebrew not found"
        echo ""
        echo "🔧 To install FFmpeg manually:"
        echo "1. Install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo ""
        echo "2. Then install FFmpeg:"
        echo "   brew install ffmpeg"
        echo ""
        echo "3. Or download FFmpeg directly from: https://ffmpeg.org/download.html"
    fi
else
    echo "🐧 Detected Linux/Unix"
    echo "📦 Try installing FFmpeg with your package manager:"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   CentOS/RHEL: sudo yum install ffmpeg"
    echo "   Arch: sudo pacman -S ffmpeg"
fi

echo ""
echo "✅ After installing FFmpeg, restart the app with: python3 app.py"
