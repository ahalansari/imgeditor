#!/usr/bin/env python3
"""
Test script to verify all critical fixes are working
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        print(f"✅ MPS available: {torch.backends.mps.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from diffusers import QwenImageEditPipeline
        print("✅ QwenImageEditPipeline")
    except ImportError as e:
        print(f"❌ Diffusers import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL)")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test that the Flask app can be imported and has required routes"""
    print("\n🔍 Testing app structure...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test routes exist
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/upload', '/uploads/<filename>', '/output/<filename>']
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route exists: {route}")
            else:
                print(f"❌ Missing route: {route}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n🔍 Testing directories...")
    
    import os
    required_dirs = ['uploads', 'output', 'templates']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Missing directory: {dir_name}/")
            return False
    
    # Test template files
    template_files = ['templates/index.html', 'templates/result.html']
    for template in template_files:
        if os.path.exists(template):
            print(f"✅ Template exists: {template}")
        else:
            print(f"❌ Missing template: {template}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Running Qwen Image Editor Tests")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("App Structure Tests", test_app_structure), 
        ("Directory Tests", test_directories)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            all_passed = False
        print()
    
    print("=" * 40)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("🚀 Ready to run: python run.py")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Check the errors above and fix them")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())