@echo off
echo ================================================================================
echo Shannon Stock Analyzer - 全自动扫描
echo ================================================================================
echo.
echo 将自动执行:
echo   1. 下载全市场数据 (180天, 5000+ 只股票)
echo   2. 扫描Shannon候选 (MCDX + Ichimoku + Volume)
echo   3. 导出结果到 results/ 文件夹
echo.
echo 预计时间: 40-60 分钟
echo.
pause

echo.
echo 步骤 1/2: 下载数据...
echo.
python scripts/download/download_all_stocks.py

echo.
echo 步骤 2/2: 扫描Shannon...
echo.
python scripts/find_all_shannon.py

echo.
echo ================================================================================
echo 完成！
echo ================================================================================
echo.
echo 结果已保存到 results/ 文件夹
echo.
explorer results

pause
