#!/usr/bin/env python3
"""
Simple test script to verify the setup
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    load_dotenv()
    
    print("🔍 Testing Environment Setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy env.example to .env and add your API key")
        return False
    
    # Check API key
    api_key = os.getenv('SARVAM_API_KEY')
    if not api_key or api_key == 'your_sarvam_api_key_here':
        print("❌ SARVAM_API_KEY not set!")
        print("   Please add your Sarvam AI API key to .env file")
        return False
    
    # Check PIN
    pin = os.getenv('SECRET_PIN')
    if not pin:
        print("❌ SECRET_PIN not set!")
        return False
    
    print("✅ Environment variables configured correctly")
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n📦 Testing Package Imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import sarvamai
        print("✅ SarvamAI imported successfully")
    except ImportError:
        print("❌ SarvamAI not installed")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    return True

def test_ffmpeg():
    """Test if ffmpeg is available"""
    print("\n🎬 Testing FFmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg not found")
        print("   Please install FFmpeg: https://ffmpeg.org/download.html")
        return False

def main():
    """Run all tests"""
    print("🚀 Voice-to-Text Setup Test")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_imports,
        test_ffmpeg
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! You're ready to run the app.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:8080")
        print("3. Enter your PIN and start recording!")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
