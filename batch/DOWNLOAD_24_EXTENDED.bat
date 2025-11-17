@echo off
echo ================================================================================
echo 下载24只金叉股票扩展数据
echo ================================================================================
echo.
echo 股票数量: 24 只
echo 数据范围: 最近120天
echo 目标: 至少80天数据 (用于Ichimoku分析)
echo.
echo Ichimoku需要: 52 + 26 = 78 天
echo.
echo 开始下载...
echo.

python download_24_stocks_extended.py

echo.
pause
