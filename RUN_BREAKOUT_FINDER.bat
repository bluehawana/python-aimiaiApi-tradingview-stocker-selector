@echo off
echo ========================================
echo 突破股票筛选器 - 4大严格标准
echo ========================================
echo.
echo 筛选标准:
echo 1. 近2-3个月接近金叉
echo 2. 成交量 >= 3x 正常日均量
echo 3. MCDX: PC >= 95%%, SMA PC >= 80%%
echo 4. 当天涨幅 >= 5%%
echo.
echo 开始扫描...
echo.

REM 运行筛选器
python find_breakout_stocks.py

echo.
echo ========================================
echo 筛选完成！
echo ========================================
pause
