@echo off
echo ================================================================================
echo 全市场Shannon扫描 - 终极版
echo ================================================================================
echo.
echo 扫描范围: 全市场 5000+ 只A股
echo.
echo 分析指标:
echo   1. MCDX金叉 (40分)
echo   2. Ichimoku Cloud (30分) - 价格突破云层 + 云层转为看涨
echo   3. 成交量暴增 (20分) - >= 2.5x
echo   4. 价格涨幅 (10分)
echo.
echo 筛选标准:
echo   - 必须金叉 (SMA PC > SMA LC)
echo   - 综合评分 >= 40分
echo.
echo 输出:
echo   - 超级信号 (>=80分)
echo   - 强烈推荐 (60-79分)
echo   - 值得关注 (40-59分)
echo.
echo 开始扫描...
echo.

python find_all_shannon.py

echo.
pause
