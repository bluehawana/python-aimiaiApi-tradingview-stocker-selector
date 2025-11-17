@echo off
cd ..
echo ================================================================================
echo 全自动Shannon扫描 - 一键运行
echo ================================================================================
echo.
echo 将自动执行:
echo   1. 下载全市场数据 (180天)
echo   2. 扫描Shannon候选
echo   3. 打开结果文件夹
echo.
echo 预计时间: 40-60 分钟
echo.
echo 开始执行...
echo.

python scripts/automation/auto_scan_complete.py

pause
