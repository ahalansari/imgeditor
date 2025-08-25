#!/usr/bin/env python3
"""
Optimized startup script for Qwen Image Editor
Handles model loading gracefully and provides better error messages
"""

import os
import sys
import time
from app import app

def main():
    print("🚀 Starting Qwen Image Editor...")
    print("=" * 50)
    
    # Check if we're on Mac M4 Max
    try:
        import torch
        if torch.backends.mps.is_available():
            print("✅ Mac M4 Max detected with MPS acceleration")
        else:
            print("⚠️  MPS not available - using CPU")
    except ImportError:
        print("❌ PyTorch not found")
        return 1
    
    print("\n📱 Starting web server...")
    print("🌐 Open your browser to: http://localhost:5001")
    print("📁 Upload folder: uploads/")
    print("📁 Output folder: output/")
    print("\n💡 Tip: Use specific prompts like:")
    print("   - 'Change the background to a sunset'")
    print("   - 'Make the car red instead of blue'")
    print("   - 'Add sunglasses to the person'")
    print("\n" + "=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
