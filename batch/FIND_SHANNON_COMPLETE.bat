@echo off
echo ================================================================================
echo 完整Shannon扫描流程 - 全市场
echo ================================================================================
echo.
echo 流程:
echo   1. 下载全市场A股数据 (如需要)
echo   2. 扫描所有金叉股票
echo   3. 分析Shannon候选 (标准2-4)
echo.
echo ================================================================================
echo.

:MENU
echo 请选择操作:
echo.
echo   1. 下载全市场数据 (首次使用或更新数据)
echo   2. 扫描金叉股票 (全市场)
echo   3. 分析Shannon候选 (已有金叉股票)
echo   4. 完整流程 (1+2+3)
echo   0. 退出
echo.
set /p choice="请输入选择 (0-4): "

if "%choice%"=="1" goto DOWNLOAD
if "%choice%"=="2" goto SCAN
if "%choice%"=="3" goto ANALYZE
if "%choice%"=="4" goto COMPLETE
if "%choice%"=="0" goto END
goto MENU

:DOWNLOAD
echo.
echo ================================================================================
echo 步骤 1: 下载全市场数据
echo ================================================================================
echo.
python download_all_stocks.py
echo.
pause
goto MENU

:SCAN
echo.
echo ================================================================================
echo 步骤 2: 扫描金叉股票
echo ================================================================================
echo.
python find_golden_cross_all.py
echo.
pause
goto MENU

:ANALYZE
echo.
echo ================================================================================
echo 步骤 3: 分析Shannon候选
echo ================================================================================
echo.
echo 请先运行步骤2获取金叉股票列表
echo 然后手动运行: python find_next_shannon_24.py
echo.
pause
goto MENU

:COMPLETE
echo.
echo ================================================================================
echo 完整流程开始
echo ================================================================================
echo.
echo 步骤 1/3: 下载数据...
python download_all_stocks.py
echo.
echo 步骤 2/3: 扫描金叉...
python find_golden_cross_all.py
echo.
echo 步骤 3/3: 请查看结果文件，然后运行Shannon分析
echo.
pause
goto MENU

:END
echo.
echo 再见!
echo.
