#!/usr/bin/env python3
"""
Simple test to check if basic dependencies are installed
"""

import sys


def test_imports():
    """Test if required packages can be imported"""
    print("Testing Python package imports...")
    print("=" * 60)

    packages = [
        ('pandas', 'Data processing'),
        ('numpy', 'Numerical computing'),
        ('requests', 'HTTP client'),
        ('yaml', 'YAML parser (PyYAML)'),
        ('dotenv', 'Environment variables (python-dotenv)'),
        ('akshare', 'China stock data'),
    ]

    success_count = 0
    failed_packages = []

    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package:<15} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {package:<15} - {description} (NOT INSTALLED)")
            failed_packages.append(package)

    print("=" * 60)
    print(f"\nResults: {success_count}/{len(packages)} packages available")

    if failed_packages:
        print("\n⚠️  Missing packages. Install with:")
        print(f"   pip install {' '.join(failed_packages)}")
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True


def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("\n" + "=" * 60)
    print("Testing basic MCDX calculation logic...")
    print("=" * 60)

    try:
        import numpy as np

        # Test clamp function
        def clamp(x, minv, maxv):
            return max(minv, min(maxv, x))

        assert clamp(50, 0, 100) == 50
        assert clamp(-10, 0, 100) == 0
        assert clamp(150, 0, 100) == 100
        print("✅ Clamp function works correctly")

        # Test basic array operations
        test_array = np.array([10, 20, 30, 40, 50])
        assert test_array.mean() == 30
        assert test_array.min() == 10
        assert test_array.max() == 50
        print("✅ NumPy array operations work correctly")

        print("\n✅ Basic functionality test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Basic functionality test failed: {e}")
        return False


def main():
    """Main test function"""
    print("\n🔍 AI Stock Analyzer - Dependency Check")
    print(f"Python version: {sys.version}")
    print()

    # Test imports
    imports_ok = test_imports()

    if not imports_ok:
        print("\n" + "=" * 60)
        print("📦 Installation Instructions")
        print("=" * 60)
        print("\n1. Install all dependencies at once:")
        print("   pip install -r requirements.txt")
        print("\n2. Or install individually:")
        print("   pip install pandas numpy requests PyYAML python-dotenv akshare")
        print("\n3. After installation, run this test again:")
        print("   python test_simple.py")
        return 1

    # Test basic functionality
    func_ok = test_basic_functionality()

    if imports_ok and func_ok:
        print("\n" + "=" * 60)
        print("✅ All tests passed! Ready to run full test.")
        print("=" * 60)
        print("\nNext step:")
        print("   python test_china_mcdx.py")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
