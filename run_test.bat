@echo off
echo ========================================
echo China Stock Market MCDX Analyzer Test
echo ========================================
echo.
echo Testing data fetch and MCDX calculation...
echo.

python test_china_mcdx.py

echo.
echo ========================================
echo Test completed!
echo ========================================
echo.
echo Next steps:
echo 1. Review the results above
echo 2. Configure your API credentials in .env
echo 3. Run: python main.py --web
echo 4. Open browser to: http://localhost:5000
echo.
pause
