@echo off
echo ========================================
echo Installing AI Stock Analyzer - Step by Step
echo ========================================
echo.
echo Python version:
python --version
echo.

echo ========================================
echo Step 1: Upgrading pip
echo ========================================
python -m pip install --upgrade pip
echo.

echo ========================================
echo Step 2: Installing core packages
echo ========================================
pip install numpy==1.24.4
pip install pandas==1.5.3
echo.

echo ========================================
echo Step 3: Installing HTTP and config packages
echo ========================================
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install PyYAML==6.0.1
echo.

echo ========================================
echo Step 4: Installing China stock data package
echo ========================================
pip install akshare==1.11.84
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.

echo Running diagnostic...
python diagnose.py

echo.
pause
