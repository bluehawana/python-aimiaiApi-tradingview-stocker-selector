@echo off
echo ================================================================================
echo Shannon + Ichimoku 综合分析
echo ================================================================================
echo.
echo 分析指标:
echo   1. MCDX (40分) - Profit Chips, SMA PC, Locked Chips
echo   2. Ichimoku (30分) - 云层突破, 强烈看涨信号
echo   3. 成交量 (20分) - 成交量比率
echo   4. 价格 (10分) - 5日涨幅
echo.
echo 超级信号:
echo   💎 Ichimoku强势 + MCDX金叉 + 成交量放大
echo   = 价格突破云层 + 云层转为看涨 + PC>=80%% + 量>=2x
echo.
echo 开始分析...
echo.

python find_shannon_with_ichimoku.py

echo.
pause
