@echo off
echo ========================================
echo Installing AI Stock Analyzer Dependencies
echo ========================================
echo.

echo Checking Python version...
python --version
echo.

echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.

echo Running dependency check...
python test_simple.py

echo.
pause
