@echo off
echo ================================================================================
echo 在24只金叉股票中寻找下一个Shannon
echo ================================================================================
echo.
echo 分析标准:
echo   标准1: 金叉 (已完成筛选)
echo   标准2: 成交量暴增 (>=2.5x, 持续2天+)
echo   标准3: 价格突破 (涨幅、均线排列)
echo   标准4: MCDX指标 (PC>=80%%, SMA PC>=85%%, LC<15%%)
echo.
echo 评分系统:
echo   - 成交量: 40分
echo   - 价格:   30分
echo   - MCDX:   30分
echo   - 总分:   100分
echo.
echo 开始分析...
echo.

python find_next_shannon_24.py

echo.
pause
