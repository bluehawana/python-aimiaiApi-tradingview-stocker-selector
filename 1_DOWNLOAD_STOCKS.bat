@echo off
echo ========================================
echo 下载中国A股数据 - 最近3个月
echo ========================================
echo.
echo 使用 akshare (免费，无需API)
echo.
echo 覆盖板块:
echo - 芯片半导体、存储芯片、CPO光学
echo - 固态电池、六氟磷酸锂、储能
echo - 光伏、智能电网、机器人
echo - 新能源汽车
echo.
echo 总计: 50+ 只股票
echo.
echo 开始下载...
echo.

python download_china_stocks.py

echo.
pause
