# 最近 2 周多板块热点分析指南

## 📊 功能概述

实时分析**最近 2 周**（14 天）的股票表现，重点关注：

### 1. 成交量变化

- ✅ 最近 2 周平均成交量 vs 前 2 周
- ✅ 最近 2 周最大成交量
- ✅ 暴量天数统计（成交量 > 2x 30 日均量）
- ✅ 成交量趋势（显著放量/温和放量/平稳/缩量）

### 2. MCDX 指标变化

- ✅ Profit Chips 当前值和变化
- ✅ Locked Chips 当前值和变化
- ✅ SMA 趋势分析
- ✅ 最近 2 周 MCDX 趋势（强势上升/上升/稳定/下降）

### 3. 技术信号

- ✅ Golden Cross（金叉）
- ✅ Double Dragon（双龙出海）
- ✅ Bottom Catch（底部反转）
- ✅ Volume Surge（成交量暴增）

## 🎯 覆盖板块（10 大热门赛道）

1. **芯片半导体** - 中芯国际、北方华创、韦尔股份、澜起科技、华润微
2. **存储芯片** - 紫光国微、兆易创新、寒武纪
3. **CPO 光学** - 新易盛、中际旭创、光迅科技
4. **固态电池** - 国轩高科、宁德时代、容百科技、赣锋锂业
5. **六氟磷酸锂** - 赣锋锂业、天齐锂业、亿纬锂能、恩捷股份
6. **储能** - 宁德时代、国轩高科、亿纬锂能、固德威、锦浪科技
7. **光伏** - 隆基绿能、天合光能、晶澳科技、阳光电源、福莱特
8. **智能电网** - 晶盛机电、国轩高科、锦浪科技、先导智能
9. **机器人** - 机器人、先导智能、石头科技、埃斯顿、汇川技术
10. **新能源汽车** - 比亚迪、宁德时代、德赛西威、中环股份

**总计**: 50+ 只优质股票

## 🚀 快速开始

### 方式 1: 使用批处理文件（推荐）

```bash
# Windows 双击运行
RUN_2WEEKS_ANALYSIS.bat
```

### 方式 2: 命令行运行

```bash
# 基础分析（热度 >= 50）
python analyze_recent_2weeks.py

# 高标准筛选（热度 >= 60）
python analyze_recent_2weeks.py --min-score 60

# 分析最近10天
python analyze_recent_2weeks.py --days 10

# 导出到指定文件
python analyze_recent_2weeks.py --export results/my_analysis.csv
```

## 📈 热度评分系统（0-100 分）

### MCDX 指标（30 分）

- Profit Chips >= 90%: 15 分
- Profit Chips >= 80%: 10 分
- Profit Chips >= 70%: 5 分
- Locked Chips < 10%: 10 分
- Locked Chips < 20%: 5 分
- SMA PC > SMA LC: 5 分

### 最近 2 周 MCDX 趋势（20 分）

- 强势上升（PC +10%以上）: 20 分
- 上升（PC +5%以上）: 15 分
- 稳定: 5 分

### 最近 2 周成交量（30 分）

- 显著放量（1.5x 以上）: 20 分
- 温和放量（1.2x 以上）: 15 分
- 平稳: 5 分
- 暴量天数 >= 3 天: 10 分
- 暴量天数 >= 2 天: 5 分

### 技术信号（20 分）

- Golden Cross: 10 分
- Double Dragon: 5 分
- Bottom Catch: 5 分

## 📊 输出示例

```
🔥 300750 - solid_state_battery
================================================================================
热度评分: 85.5/100
日期: 2024-11-17
价格: ¥245.80 (+8.5% 近2周)

📈 MCDX 指标:
  Profit Chips: 92.3% (SMA: 88.5%)
  Locked Chips: 4.2% (SMA: 6.1%)
  行为模式: Strong Hold
  建议: BUY
  最近2周趋势: 强势上升 (PC变化: +12.5%)

📊 成交量分析:
  最新成交量: 125.5M
  30日平均: 38.2M
  成交量比率: 3.28x
  最近2周趋势: 显著放量
  2周平均成交量: 95.3M
  2周最大成交量: 145.8M
  暴量天数(>2x): 8 天

🎯 技术信号:
  ✨ Golden Cross, 🐉 Double Dragon, 🔥 Volume Surge
```

## 🔍 分析逻辑

### 1. 数据获取

- 获取最近 60 天数据（用于计算 30 日均量基准）
- 提取最近 14 天数据进行重点分析

### 2. MCDX 分析

```python
# 计算当前 MCDX
mcdx_current = calculate_mcdx(data_60days)

# 计算2周前 MCDX
mcdx_2weeks_ago = calculate_mcdx(data_46days)

# 计算变化
pc_change = mcdx_current.profit_chips - mcdx_2weeks_ago.profit_chips
```

### 3. 成交量分析

```python
# 最近2周平均成交量
avg_volume_2w = recent_14days['volume'].mean()

# 前2周平均成交量
avg_volume_prev = previous_14days['volume'].mean()

# 成交量变化比率
volume_change_ratio = avg_volume_2w / avg_volume_prev

# 暴量天数统计
spike_days = count(volume > avg_30d * 2.0)
```

### 4. 热度评分

```python
hot_score = (
    mcdx_score(30分) +
    mcdx_trend_score(20分) +
    volume_score(30分) +
    signal_score(20分)
)
```

## 📁 输出文件

### 自动导出

```
results/recent_2weeks_20241117_143025.csv
```

### CSV 包含字段

- symbol: 股票代码
- sector: 所属板块
- latest_date: 最新日期
- latest_close: 最新价格
- price_change_2w: 2 周价格变化%
- profit_chips: Profit Chips
- locked_chips: Locked Chips
- volume_ratio: 成交量比率
- mcdx_trend_2w: MCDX 2 周趋势
- volume_trend_2w: 成交量 2 周趋势
- hot_score: 热度评分
- ... 等 30+个字段

## 🎯 使用场景

### 场景 1: 每日盘后分析

```bash
# 每天收盘后运行，找出当天热点
python analyze_recent_2weeks.py --min-score 60
```

### 场景 2: 周末复盘

```bash
# 周末分析整周表现
python analyze_recent_2weeks.py --days 7 --min-score 55
```

### 场景 3: 板块轮动追踪

```bash
# 低门槛扫描，观察板块轮动
python analyze_recent_2weeks.py --min-score 40
```

### 场景 4: 导出数据分析

```bash
# 导出到 Excel 进一步分析
python analyze_recent_2weeks.py --export results/weekly_report.csv
```

## 🔥 热度等级解读

### 🔥🔥🔥 超级热点（80-100 分）

- **特征**: MCDX 强势上升 + 显著放量 + 多个技术信号
- **建议**: 重点关注，可能是下一个突破股
- **操作**: 深入研究基本面，考虑建仓

### 🔥🔥 高热度（60-79 分）

- **特征**: MCDX 上升 + 温和放量 + 部分技术信号
- **建议**: 值得关注，观察后续表现
- **操作**: 加入自选股，持续跟踪

### 🔥 中等热度（50-59 分）

- **特征**: MCDX 稳定 + 成交量平稳 + 少量信号
- **建议**: 观察为主
- **操作**: 等待更明确信号

### ⚪ 低热度（< 50 分）

- **特征**: 指标一般，无明显突破迹象
- **建议**: 暂不关注
- **操作**: 继续观察其他标的

## ⚙️ 自定义配置

### 调整分析天数

```bash
# 分析最近7天
python analyze_recent_2weeks.py --days 7

# 分析最近30天
python analyze_recent_2weeks.py --days 30
```

### 调整热度阈值

```bash
# 只看超级热点
python analyze_recent_2weeks.py --min-score 80

# 看所有股票
python analyze_recent_2weeks.py --min-score 0
```

### 修改板块配置

编辑 `config_multi_sector.yaml`:

```yaml
stocks:
  sectors:
    my_sector:
      - "600000"
      - "000001"
```

## 📊 与 Shannon Pattern 的区别

| 特性     | Shannon Pattern        | Recent 2 Weeks    |
| -------- | ---------------------- | ----------------- |
| 时间范围 | 历史模式（9 月 11-12） | 最近 2 周实时数据 |
| 关注点   | 历史突破模式           | 当前热点趋势      |
| 成交量   | 3x 暴增（89M vs 30M）  | 2 周变化趋势      |
| MCDX     | PC=100, SMA=86.65      | 2 周变化趋势      |
| 用途     | 寻找历史相似模式       | 发现当前热点      |
| 更新频率 | 按需运行               | 每日盘后          |

## 🔧 故障排除

### 问题 1: 数据获取失败

**解决方案**:

```bash
# 测试 API 连接
python test_bearer_auth.py

# 检查 .env 配置
cat .env
```

### 问题 2: 没有找到热点股票

**解决方案**:

- 降低 `--min-score` 阈值
- 检查是否是交易日
- 确认数据是否最新

### 问题 3: 分析速度慢

**原因**: 需要获取 50+只股票的数据

**优化**:

- 减少板块数量
- 使用缓存（待实现）
- 分批次运行

## 📝 注意事项

1. **交易日数据**: 只在交易日有新数据
2. **数据延迟**: 可能有 15-30 分钟延迟
3. **API 限制**: 注意 aimiai.com API 调用频率
4. **风险提示**: 仅供参考，不构成投资建议

## 🎯 最佳实践

### 每日工作流

```bash
# 1. 早盘前：查看昨日热点
python analyze_recent_2weeks.py --min-score 60

# 2. 盘中：关注热点股票实时表现

# 3. 盘后：更新分析，导出报告
python analyze_recent_2weeks.py --export results/daily_$(date +%Y%m%d).csv
```

### 周末复盘

```bash
# 1. 分析整周表现
python analyze_recent_2weeks.py --days 7 --min-score 50

# 2. 对比上周数据
# 查看板块轮动情况

# 3. 制定下周策略
```

## 📞 支持

如有问题：

1. 查看 `BEARER_AUTH_UPDATE.md` - API 认证
2. 运行 `python test_bearer_auth.py` - 测试连接
3. 检查日志文件

---

**开始分析最近 2 周热点！** 🚀

```bash
python analyze_recent_2weeks.py
```
