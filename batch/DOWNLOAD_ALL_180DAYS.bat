@echo off
echo ================================================================================
echo 下载全市场A股数据 - 180天
echo ================================================================================
echo.
echo 覆盖范围:
echo   - 上海证券交易所 (主板 + 科创板)
echo   - 深圳证券交易所 (主板 + 创业板)
echo   - 总计: 5000+ 只股票
echo.
echo 数据范围: 最近180天 (6个月)
echo 用途: Shannon + Ichimoku综合分析
echo.
echo 预计时间: 30-40 分钟
echo.
echo 注意:
echo   - 需要 Tushare Token
echo   - 已存在的数据会自动跳过
echo   - 建议在网络稳定时运行
echo.
set /p confirm="确认开始下载? (Y/N): "
if /i not "%confirm%"=="Y" goto END

echo.
echo 开始下载...
echo.

python download_all_stocks.py

:END
echo.
pause
