#!/usr/bin/env python3
"""
Diagnostic script to identify issues with the AI Stock Analyzer setup
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Python Version Check")
    print("-" * 60)
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print("   Please upgrade Python")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_pip():
    """Check if pip is available"""
    print("\n📦 Pip Check")
    print("-" * 60)
    try:
        import pip
        print(f"✅ Pip is installed (version: {pip.__version__})")
        return True
    except ImportError:
        print("❌ Pip is not installed")
        print("   Install pip: https://pip.pypa.io/en/stable/installation/")
        return False


def check_files():
    """Check if required files exist"""
    print("\n📁 File Structure Check")
    print("-" * 60)

    required_files = [
        'requirements.txt',
        'config.yaml',
        '.env',
        'src/data/china_stock_api.py',
        'src/mcdx/calculator.py',
        'test_china_mcdx.py',
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False

    return all_exist


def check_env_file():
    """Check .env file configuration"""
    print("\n🔐 Environment Configuration Check")
    print("-" * 60)

    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found")
        return False

    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_app_id = 'AIMIAI_APP_ID' in content
    has_app_key = 'AIMIAI_APP_KEY' in content

    if has_app_id:
        print("✅ AIMIAI_APP_ID is configured")
    else:
        print("⚠️  AIMIAI_APP_ID not found in .env")

    if has_app_key:
        print("✅ AIMIAI_APP_KEY is configured")
    else:
        print("⚠️  AIMIAI_APP_KEY not found in .env")

    if 'your_app_id_here' in content or 'your_app_key_here' in content:
        print("⚠️  Placeholder values detected - please update with real credentials")
        return False

    return has_app_id and has_app_key


def check_packages():
    """Check if required packages are installed"""
    print("\n📚 Package Installation Check")
    print("-" * 60)

    required_packages = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'requests': 'HTTP client',
        'yaml': 'YAML parser',
        'dotenv': 'Environment variables',
        'akshare': 'China stock data',
    }

    optional_packages = {
        'tushare': 'Alternative China stock data',
        'flask': 'Web framework',
        'plotly': 'Advanced charting',
    }

    installed = []
    missing = []

    print("Required packages:")
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<15} - {description}")
            installed.append(package)
        except ImportError:
            print(f"  ❌ {package:<15} - {description} (NOT INSTALLED)")
            missing.append(package)

    print("\nOptional packages:")
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<15} - {description}")
        except ImportError:
            print(f"  ⚠️  {package:<15} - {description} (not installed)")

    return len(missing) == 0, missing


def print_solution(missing_packages):
    """Print solution steps"""
    print("\n" + "=" * 60)
    print("🔧 SOLUTION STEPS")
    print("=" * 60)

    if missing_packages:
        print("\n1. Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\n   OR install all at once:")
        print("   pip install -r requirements.txt")

    print("\n2. Configure API credentials:")
    print("   - Edit .env file")
    print("   - Get credentials from: https://aimiai.com/console")
    print("   - Replace placeholder values with real credentials")

    print("\n3. Run tests:")
    print("   python test_simple.py")
    print("   python test_china_mcdx.py")


def main():
    """Main diagnostic function"""
    print("\n" + "=" * 60)
    print("🔍 AI Stock Analyzer - System Diagnostic")
    print("=" * 60)

    results = []

    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Pip", check_pip()))
    results.append(("File Structure", check_files()))
    results.append(("Environment Config", check_env_file()))

    packages_ok, missing = check_packages()
    results.append(("Required Packages", packages_ok))

    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)

    all_ok = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<25} {status}")
        if not result:
            all_ok = False

    if all_ok:
        print("\n✅ All checks passed! System is ready.")
        print("\nNext step:")
        print("   python test_china_mcdx.py")
        return 0
    else:
        print("\n❌ Some checks failed. See solutions below.")
        print_solution(missing)
        return 1


if __name__ == "__main__":
    sys.exit(main())
