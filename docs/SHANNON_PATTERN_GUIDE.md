# Shannon Pattern Finder Guide

## 什么是 Shannon Pattern？

Shannon Pattern 是一种强势股票突破模式，特征包括：

### 关键特征（2024 年 9 月 11-12 日 Shannon 案例）

1. **成交量暴增**

   - 正常日成交量：约 30M
   - 突破日成交量：89M
   - 成交量比率：3x（300%）
   - 持续时间：至少 2 天

2. **MCDX 指标**

   - 红色柱状图（Profit Chips）：达到 100%
   - 深红色线（SMA Profit Chips）：约 86.65%
   - 锁定筹码（Locked Chips）：< 15%

3. **价格行为**
   - 上升趋势
   - 突破关键阻力位
   - 伴随成交量放大

## 覆盖行业板块

本系统覆盖以下热门板块：

### 1. 半导体芯片 (Chips & Memory)

- 中芯国际 (688981)
- 北方华创 (002371)
- 韦尔股份 (603501)
- 紫光国微 (002049)
- 兆易创新 (603986)

### 2. CPO 共封装光学

- 新易盛 (300502)
- 中际旭创 (300308)
- 光迅科技 (002281)

### 3. 固态电池

- 国轩高科 (002074)
- 宁德时代 (300750)
- 容百科技 (688005)
- 赣锋锂业 (002460)

### 4. 六氟磷酸锂

- 赣锋锂业 (002460)
- 天齐锂业 (002466)
- 亿纬锂能 (300014)
- 恩捷股份 (002812)

### 5. 储能 (Energy Storage)

- 宁德时代 (300750)
- 国轩高科 (002074)
- 固德威 (688390)
- 锦浪科技 (300763)

### 6. 光伏 (Solar Energy)

- 隆基绿能 (601012)
- 天合光能 (688599)
- 晶澳科技 (002459)
- 阳光电源 (300274)

### 7. 智能电网 (Smart Grid)

- 晶盛机电 (300316)
- 先导智能 (300450)

### 8. 机器人 (Robotics)

- 机器人 (300024)
- 石头科技 (688169)
- 埃斯顿 (002747)
- 汇川技术 (300124)

### 9. 新能源汽车

- 比亚迪 (002594)
- 德赛西威 (002920)

## 快速开始

### 1. 配置 API 凭证

确保 `.env` 文件包含你的 aimiai.com API 凭证：

```bash
AppId=你的_app_id
AppKey=你的_app_key
```

### 2. 运行 Shannon Pattern 扫描

```bash
# 扫描所有板块，找出 Shannon Score >= 60 的股票
python find_shannon_pattern.py

# 自定义最低分数阈值
python find_shannon_pattern.py --min-score 70

# 指定配置文件
python find_shannon_pattern.py --config config_multi_sector.yaml

# 导出结果到 CSV
python find_shannon_pattern.py --export results/my_results.csv
```

### 3. 查看结果

程序会显示：

- Shannon Score（0-100 分）
- MCDX 指标（Profit Chips, Locked Chips）
- 成交量分析（当前成交量 vs 30 日平均）
- 技术信号（Golden Cross, Double Dragon, Bottom Catch）

## Shannon Score 评分标准

### MCDX 部分（40 分）

- Profit Chips >= 95%：20 分
- Profit Chips >= 86%：15 分
- Profit Chips >= 80%：10 分
- SMA Profit Chips >= 85%：15 分
- SMA Profit Chips >= 80%：10 分
- Locked Chips < 5%：5 分

### 成交量部分（40 分）

- 成交量比率 >= 3.0x：25 分
- 成交量比率 >= 2.5x：20 分
- 成交量比率 >= 2.0x：15 分
- 成交量暴增（Surge）：10 分
- 成交量趋势上升：5 分

### 模式识别（20 分）

- 检测到 Shannon Pattern：15 分
- Golden Cross 或 Double Dragon：5 分

## 筛选标准

默认筛选条件（可在 `config_multi_sector.yaml` 中修改）：

```yaml
screening:
  criteria:
    min_profit_chips: 80 # PC > 80%
    max_locked_chips: 15 # LC < 15%
    min_volume_ratio: 2.5 # 成交量 > 2.5x 平均
    min_volume_surge_days: 2 # 至少持续2天
    min_price_change: 0.02 # +2% 最低涨幅
    require_uptrend: true # 必须处于上升趋势
```

## 使用 aimiai.com API

### 认证方式

**步骤 1: 获取 Token**

POST 请求到 `https://aimiai.com/api/token/get`

```json
{
  "appId": "你的_app_id",
  "appKey": "你的_app_key"
}
```

**步骤 2: 使用 Token**

在业务接口请求头中添加：

```
Authorization: Bearer {token}
```

⚠️ **注意**: `Bearer` 后面有一个空格！

### API 端点

- 获取 Token: `POST /api/token/get`
  - 请求体: `{"appId": "...", "appKey": "..."}`
  - 返回: `{"code": 200, "data": "token字符串"}`
- 获取 K 线数据: `POST /api/stock/kline`
- 获取股票列表: `POST /api/stock/list`
- 获取实时行情: `POST /api/stock/quote`

## 结果解读

### Shannon Score >= 80

🔥 **强烈推荐** - 非常接近 Shannon 模式

- 成交量暴增 3x+
- MCDX 指标极佳
- 多个技术信号确认

### Shannon Score 60-79

✨ **值得关注** - 具有 Shannon 模式特征

- 成交量明显放大
- MCDX 指标良好
- 部分技术信号确认

### Shannon Score 40-59

⚠️ **观察** - 有潜力但需确认

- 成交量有所放大
- MCDX 指标一般
- 等待更多信号

### Shannon Score < 40

❌ **不符合** - 不符合 Shannon 模式

## 注意事项

1. **风险提示**：本工具仅供参考，不构成投资建议
2. **数据延迟**：数据可能有延迟，请以实时行情为准
3. **API 限制**：注意 aimiai.com API 的调用频率限制
4. **市场风险**：股市有风险，投资需谨慎

## 高级用法

### 自定义板块扫描

编辑 `config_multi_sector.yaml`，添加或修改板块：

```yaml
stocks:
  sectors:
    my_custom_sector:
      - "600000"
      - "000001"
```

### 调整检测参数

```yaml
technical_analysis:
  volume_params:
    volume_ratio_surge: 3.0 # 调整暴增阈值
    lookback_days: 30 # 调整回看天数

  mcdx_params:
    profit_chips_threshold: 86.65 # 调整 PC 阈值
```

## 故障排除

### 问题：无法获取 Token

- 检查 `.env` 文件中的 AppId 和 AppKey
- 确认 aimiai.com API 凭证有效
- 检查网络连接

### 问题：没有找到符合条件的股票

- 降低 `--min-score` 阈值
- 检查配置文件中的筛选条件
- 确认股票代码正确

### 问题：数据获取失败

- 检查 aimiai.com API 是否正常
- 确认股票代码格式正确（6 位数字）
- 查看日志文件了解详细错误

## 联系支持

如有问题，请检查：

1. `.env` 配置
2. `config_multi_sector.yaml` 设置
3. 日志文件 `logs/` 目录

---

**祝你找到下一个 Shannon！** 🚀
