# 快速开始 - 中国股市 MCDX 分析

## 🇨🇳 中国 A 股市场分析器

这个工具可以分析上海证券交易所（SSE）和深圳证券交易所（SZSE）的股票，使用 MCDX（市场筹码分布）指标来识别买入/卖出/持有信号。

## 📋 前置要求

- Python 3.8 或更高版本
- aimiai.com API 凭证（appId 和 appKey）

## 🚀 快速安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：

- `akshare` - 免费的中国股市数据源（无需 API 密钥）
- `pandas` - 数据处理
- `Flask` - Web 可视化界面

### 2. 配置 API 凭证

编辑 `.env` 文件，添加你的 aimiai.com 凭证：

```env
AIMIAI_APP_ID=你的_app_id
AIMIAI_APP_KEY=你的_app_key
```

从这里获取凭证：https://aimiai.com/console

### 3. 测试中国股市数据和 MCDX 计算

```bash
python test_china_mcdx.py
```

这将：

- ✅ 测试从上海/深圳交易所获取股票数据
- ✅ 计算 MCDX 指标（利润筹码、浮动筹码、锁定筹码）
- ✅ 检测金叉/死叉信号
- ✅ 分类股票行为（吸筹、派发、强势持有等）
- ✅ 生成买入/卖出/持有建议

## 📊 MCDX 指标说明

### 什么是 MCDX？

MCDX（Market Chip Distribution X）是一个分析市场筹码分布的技术指标，通过分析不同类型持有者的筹码百分比来判断股票的买卖时机。

### 三种筹码类型

1. **利润筹码（Profit Chips）** - 红色

   - 在当前价格下盈利的筹码百分比
   - 高值（>80%）表示大部分持有者盈利，可能面临抛压

2. **浮动筹码（Float Chips）** - 黄色

   - 可以随时交易的筹码百分比
   - 代表短期交易者的持仓

3. **锁定筹码（Locked Chips）** - 绿色
   - 长期持有不会轻易卖出的筹码百分比
   - 高值表示主力资金锁仓，看好后市

### MCDX 行为分类

| 行为                          | 图标 | 信号 | 说明                                    |
| ----------------------------- | ---- | ---- | --------------------------------------- |
| **吸筹期** (Accumulation)     | 🟢   | 买入 | 利润筹码<40%，锁定筹码 ≥20%，主力在吸筹 |
| **强势持有** (Strong Hold)    | 🔵   | 持有 | 利润筹码>80%，锁定筹码<5%，强势上涨趋势 |
| **突破准备** (Breakout Ready) | 🟡   | 买入 | 利润筹码 50-80%，锁定筹码<10%，即将突破 |
| **派发期** (Distribution)     | 🔴   | 卖出 | 利润筹码>85%，下降趋势，主力在派发      |
| **中性** (Neutral)            | ⚪   | 持有 | 无明确信号                              |

### 特殊信号

- **GC (Golden Cross)** - 金叉：利润筹码均线上穿锁定筹码均线，看涨
- **DC (Death Cross)** - 死叉：利润筹码均线下穿锁定筹码均线，看跌
- **BC (Bottom Catch)** - 抄底：潜在底部形成，入场机会
- **DD (Double Dragon)** - 双龙：强烈看涨信号
- **OS (Oversold)** - 超卖：股票超卖，可能反弹
- **OB (Overbought)** - 超买：股票超买，可能回调

## 🎯 测试股票列表

测试脚本会分析以下热门中国 A 股：

### 上海证券交易所（SSE）

- **600036** - 招商银行 (China Merchants Bank)
- **600519** - 贵州茅台 (Kweichow Moutai)
- **601318** - 中国平安 (Ping An Insurance)

### 深圳证券交易所（SZSE）

- **000001** - 平安银行 (Ping An Bank)
- **002594** - 比亚迪 (BYD)
- **300750** - 宁德时代 (CATL)

## 📈 示例输出

```
📊 MCDX Analysis Summary - 2025.11.17
================================================================
Symbol     Name         Price    Behavior           Rec    PC%    LC%
--------------------------------------------------------------------------------
600036     招商银行      ¥45.23  🟢 Accumulation    🟢 BUY  35.2%  28.5%
600519     贵州茅台     ¥1850.00 🔵 Strong Hold     🟡 HOLD 82.1%   3.2%
000001     平安银行      ¥12.45  🟡 Breakout Ready  🟢 BUY  65.8%   8.3%
002594     比亚迪       ¥245.60  🔴 Distribution    🔴 SELL 88.5%  12.1%
300750     宁德时代     ¥185.30  🟢 Accumulation    🟢 BUY  38.7%  25.9%
```

## 🔧 自定义配置

编辑 `config.yaml` 来自定义分析参数：

```yaml
stocks:
  market: "CN" # 中国市场
  symbols:
    - "600036" # 添加你想分析的股票代码
    - "000001"
  china_data_source: "akshare" # 数据源

technical_analysis:
  mcdx_params:
    length: "Auto" # Auto, 34-bar, 50-bar, 100-bar
    revision: "12" # 使用最新版本12
    sma_pc_length: 10 # 利润筹码均线周期
    sma_lc_length: 10 # 锁定筹码均线周期
```

## 🌐 启动 Web 可视化界面

```bash
python main.py --web
```

然后在浏览器打开：http://localhost:5000

Web 界面功能：

- 📊 所有股票的 MCDX 概览表
- 📈 每只股票的详细 MCDX 图表
- 🎨 颜色编码的买入/卖出/持有建议
- 🔄 自动刷新（每 60 秒）
- 🔍 按推荐类型筛选

## 💡 使用建议

1. **吸筹期（🟢 Accumulation）**

   - 最佳买入时机
   - 主力资金正在建仓
   - 锁定筹码增加，利润筹码较低

2. **突破准备（🟡 Breakout Ready）**

   - 好的买入时机
   - 股票即将突破
   - 配合金叉信号更佳

3. **强势持有（🔵 Strong Hold）**

   - 持有不动
   - 强势上涨趋势
   - 等待卖出信号

4. **派发期（🔴 Distribution）**
   - 卖出时机
   - 主力资金在出货
   - 利润筹码过高，锁定筹码减少

## 🔒 安全提示

- ✅ `.env` 文件已在 `.gitignore` 中，不会被提交到 git
- ✅ API 凭证仅存储在本地
- ✅ Token 仅保存在内存中，不会写入磁盘
- ✅ Web 界面默认仅本地访问（127.0.0.1）

## 📚 更多信息

- MCDX Pine Script 源码：`mcdx_plus.pine`
- 完整文档：`README.md`
- 项目设计：`.kiro/specs/ai-stock-analyzer/design.md`

## ❓ 常见问题

**Q: 数据从哪里来？**
A: 使用 AKShare 库，免费获取上海和深圳交易所的实时数据，无需 API 密钥。

**Q: MCDX 指标准确吗？**
A: MCDX 是一个辅助工具，应结合其他技术指标和基本面分析使用。

**Q: 可以分析美股吗？**
A: 可以！在 `config.yaml` 中设置 `market: "US"` 并使用美股代码（如 AAPL, GOOGL）。

**Q: 如何添加更多股票？**
A: 编辑 `config.yaml` 的 `stocks.symbols` 列表，添加 6 位股票代码。

## 🎉 开始使用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 测试中国股市数据
python test_china_mcdx.py

# 3. 启动 Web 界面
python main.py --web

# 4. 打开浏览器
# http://localhost:5000
```

祝投资顺利！📈🚀
