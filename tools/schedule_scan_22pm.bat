@echo off
echo ================================================================================
echo 创建定时任务 - 今晚22:00自动扫描
echo ================================================================================
echo.

REM 获取当前日期和时间
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set today=%datetime:~0,8%
set current_time=%datetime:~8,4%

echo 当前时间: %datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%
echo 计划时间: %datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% 22:00
echo.

REM 创建定时任务
schtasks /create /tn "Shannon_Scan_22PM" /tr "%CD%\run_scan.bat" /sc once /st 22:00 /f

if %errorlevel% equ 0 (
    echo.
    echo ✓ 定时任务创建成功！
    echo.
    echo 任务详情:
    echo   任务名称: Shannon_Scan_22PM
    echo   执行时间: 今晚 22:00
    echo   执行脚本: run_scan.bat
    echo.
    echo 查看任务:
    echo   schtasks /query /tn "Shannon_Scan_22PM"
    echo.
    echo 删除任务:
    echo   schtasks /delete /tn "Shannon_Scan_22PM" /f
    echo.
) else (
    echo.
    echo ✗ 创建失败！请以管理员身份运行此脚本。
    echo.
    echo 右键点击此文件，选择"以管理员身份运行"
    echo.
)

pause
