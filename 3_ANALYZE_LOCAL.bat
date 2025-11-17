@echo off
echo ========================================
echo 步骤 3: 分析本地数据 - 4大标准
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

python analyze_local_data.py

echo.
pause
