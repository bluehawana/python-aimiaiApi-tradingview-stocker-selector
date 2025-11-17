@echo off
echo ================================================================================
echo 全市场金叉扫描
echo ================================================================================
echo.
echo 扫描范围: 所有A股 (5000+ 只)
echo.
echo 优先级:
echo   1. 科技股 (半导体、芯片、新能源、AI等)
echo   2. 其他行业 (银行、券商、大宗商品、基建等)
echo.
echo 筛选标准:
echo   - 已金叉: SMA PC > SMA LC
echo   - 接近金叉: Gap < 5%%
echo.
echo 开始扫描...
echo.

python find_golden_cross_all.py

echo.
pause
