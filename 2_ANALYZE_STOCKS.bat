@echo off
echo ========================================
echo 分析股票数据 - 4大严格标准
echo ========================================
echo.
echo 筛选标准:
echo 1. 近期接近金叉
echo 2. 成交量 >= 3x 正常日均量
echo 3. MCDX: PC >= 95%%, SMA PC >= 80%%
echo 4. 当天涨幅 >= 5%%
echo.
echo 开始分析...
echo.

python analyze_akshare_data.py

echo.
pause
