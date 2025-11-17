@echo off
echo ========================================
echo 使用 Tushare 下载中国A股数据
echo ========================================
echo.
echo Tushare 是最稳定的中国股票数据源
echo.
echo 首次使用需要:
echo 1. 注册: https://tushare.pro/register
echo 2. 获取 token: https://tushare.pro/user/token
echo 3. 添加到 .env 文件: TUSHARE_TOKEN=your_token
echo.
echo 开始下载...
echo.

python download_tushare.py

echo.
pause
