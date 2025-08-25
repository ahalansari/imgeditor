#!/usr/bin/env python3
"""
Optimized startup script for Qwen Image Editor - RTX 3060 version
"""

import os
import sys
import time

def check_cuda_setup():
    """Check CUDA setup and RTX 3060 compatibility"""
    try:
        import torch
        print(f"🔍 PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.version.cuda}")
            print(f"🎮 GPU: {torch.cuda.get_device_name()}")
            
            # Check VRAM
            total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"💾 Total VRAM: {total_vram:.1f} GB")
            
            if total_vram >= 10:  # RTX 3060 has ~12GB
                print("✅ VRAM sufficient for Qwen-Image-Edit")
            else:
                print("⚠️  Low VRAM - may need CPU offload")
                
            return True
        else:
            print("❌ CUDA not available - will use CPU (slow)")
            return False
            
    except ImportError:
        print("❌ PyTorch not found")
        return False

def main():
    print("🚀 Starting Qwen Image Editor (CUDA/RTX 3060 Optimized)")
    print("=" * 60)
    
    # Check CUDA setup
    cuda_available = check_cuda_setup()
    
    if cuda_available:
        print("\n🎯 RTX 3060 Performance Expectations:")
        print("   - Model loading: ~1-2 minutes (first time)")
        print("   - Image processing: ~15-30 seconds per image")
        print("   - Max image size: 1536x1536 pixels")
        print("   - VRAM usage: ~8-10GB during processing")
    else:
        print("\n⚠️  CPU Mode (slower):")
        print("   - Model loading: ~3-5 minutes")
        print("   - Image processing: ~2-5 minutes per image")
    
    # Import and start the CUDA-optimized app
    try:
        from app_cuda import app
        print("\n📱 Starting web server...")
        print("🌐 Open your browser to: http://localhost:5001")
        print("\n💡 RTX 3060 Tips:")
        print("   - Larger images supported vs Mac M4 Max")
        print("   - Faster inference with fp16 precision")
        print("   - Better memory management with CUDA")
        print("\n" + "=" * 60)
        
        app.run(debug=False, host='0.0.0.0', port=5001)  # Debug=False for better performance
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
