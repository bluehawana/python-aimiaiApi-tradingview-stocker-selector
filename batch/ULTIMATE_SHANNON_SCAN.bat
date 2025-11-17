@echo off
title 终极Shannon扫描系统
color 0A

:MENU
cls
echo ================================================================================
echo                    终极Shannon扫描系统
echo ================================================================================
echo.
echo                Shannon + Ichimoku + MCDX 三重分析
echo.
echo ================================================================================
echo.
echo 请选择操作:
echo.
echo   [1] 下载全市场数据 (180天, 5000+ 只股票)
echo   [2] 扫描全市场Shannon (推荐)
echo   [3] 扫描24只金叉股票 (快速测试)
echo   [4] 查看上次扫描结果
echo   [5] 完整流程 (下载 + 扫描)
echo.
echo   [0] 退出
echo.
echo ================================================================================
echo.
set /p choice="请输入选择 (0-5): "

if "%choice%"=="1" goto DOWNLOAD
if "%choice%"=="2" goto SCAN_ALL
if "%choice%"=="3" goto SCAN_24
if "%choice%"=="4" goto VIEW_RESULTS
if "%choice%"=="5" goto COMPLETE
if "%choice%"=="0" goto EXIT
goto MENU

:DOWNLOAD
cls
echo ================================================================================
echo 下载全市场数据
echo ================================================================================
echo.
python download_all_stocks.py
echo.
pause
goto MENU

:SCAN_ALL
cls
echo ================================================================================
echo 全市场Shannon扫描
echo ================================================================================
echo.
python find_all_shannon.py
echo.
pause
goto MENU

:SCAN_24
cls
echo ================================================================================
echo 24只金叉股票扫描
echo ================================================================================
echo.
python find_shannon_with_ichimoku.py
echo.
pause
goto MENU

:VIEW_RESULTS
cls
echo ================================================================================
echo 查看结果文件
echo ================================================================================
echo.
echo 打开 results 文件夹...
explorer results
echo.
pause
goto MENU

:COMPLETE
cls
echo ================================================================================
echo 完整流程
echo ================================================================================
echo.
echo 步骤 1/2: 下载数据...
echo.
python download_all_stocks.py
echo.
echo ================================================================================
echo 步骤 2/2: 扫描Shannon...
echo.
python find_all_shannon.py
echo.
echo ================================================================================
echo 完成!
echo ================================================================================
echo.
pause
goto MENU

:EXIT
cls
echo.
echo 感谢使用终极Shannon扫描系统!
echo.
echo 祝您找到下一个Shannon! 🚀
echo.
timeout /t 2 >nul
exit

