@echo off
echo ========================================
echo 步骤 1: 导入本地数据文件
echo ========================================
echo.
echo 将从桌面导入以下文件:
echo - 20251106.zip
echo - 20251107.zip
echo - 20251110.zip
echo - 20251111.zip
echo - 20251112.zip
echo - 20251113.zip
echo - 20251114.zip
echo - 20251117.zip
echo.
echo 目标目录: data\local\
echo.
pause

python import_local_data.py

echo.
pause
