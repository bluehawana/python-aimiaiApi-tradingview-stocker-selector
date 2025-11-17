@echo off
title 全自动Shannon扫描 - 运行中...
color 0A

echo ================================================================================
echo                    全自动Shannon扫描系统
echo ================================================================================
echo.
echo 自动执行流程:
echo   1. 下载全市场数据 (180天, 5000+ 只股票)
echo   2. 扫描Shannon候选 (Shannon + Ichimoku + MCDX)
echo   3. 导出结果到 results/ 文件夹
echo.
echo ================================================================================
echo.
echo 开始执行...
echo.

echo ================================================================================
echo 步骤 1/2: 下载全市场数据
echo ================================================================================
echo.
echo 正在下载数据，请稍候...
echo 预计时间: 30-40 分钟
echo.

python download_all_stocks.py

if errorlevel 1 (
    echo.
    echo ❌ 下载失败！请检查:
    echo    1. Tushare Token 是否配置
    echo    2. 网络连接是否正常
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ 数据下载完成
echo.

echo ================================================================================
echo 步骤 2/2: 扫描Shannon候选
echo ================================================================================
echo.
echo 正在扫描全市场，请稍候...
echo 预计时间: 10-15 分钟
echo.

python find_all_shannon.py

if errorlevel 1 (
    echo.
    echo ❌ 扫描失败！
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ 扫描完成
echo.

echo ================================================================================
echo 🎉 全部完成！
echo ================================================================================
echo.
echo 结果文件已保存到 results/ 文件夹:
echo   - all_shannon_*.csv      (全部候选)
echo   - super_shannon_*.csv    (超级信号, >=80分)
echo   - tech_shannon_*.csv     (科技股候选)
echo.
echo 正在打开结果文件夹...
echo.

timeout /t 2 >nul
explorer results

echo.
echo 按任意键退出...
pause >nul
