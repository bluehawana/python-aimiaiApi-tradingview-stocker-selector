@echo off
echo ================================================================================
echo 下载全市场A股数据
echo ================================================================================
echo.
echo 覆盖范围:
echo   - 主板、创业板、科创板、北交所
echo   - 所有行业: 科技、银行、券商、大宗商品、基建等
echo   - 总计: 5000+ 只股票
echo.
echo 数据范围: 最近3个月
echo.
echo 注意:
echo   - 需要 Tushare Token (在 .env 文件中配置)
echo   - 下载时间约 20-30 分钟
echo   - 已存在的数据会自动跳过
echo.
echo 开始下载...
echo.

python download_all_stocks.py

echo.
pause
