@echo off
cls
echo ========================================
echo AI Stock Analyzer - Quick Install
echo ========================================
echo.
echo Your Python: 3.9.13
echo Status: pandas-ta removed, now compatible!
echo.
echo ========================================
echo Installing packages...
echo ========================================
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Verifying installation...
echo ========================================
echo.

python diagnose.py

echo.
echo ========================================
echo Done! Check results above.
echo ========================================
echo.
echo Next step: python test_china_mcdx.py
echo.
pause
