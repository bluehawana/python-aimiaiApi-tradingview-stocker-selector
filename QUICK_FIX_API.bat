@echo off
echo ========================================
echo API 快速诊断和修复
echo ========================================
echo.

echo [步骤 1] 运行简单测试...
python test_api_connection.py

echo.
echo ========================================
echo.
echo 如果上面的测试失败，请尝试:
echo 1. 编辑 .env 文件，删除 token 行
echo 2. 重新运行此脚本
echo 3. 或运行详细诊断: python diagnose_api.py
echo.
echo ========================================
pause
