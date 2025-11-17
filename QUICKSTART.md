# 🚀 快速开始

## 一键运行

```bash
# Windows
run_scan.bat

# 或使用Python
python scripts/find_all_shannon.py
```

## 📋 前置要求

1. **Python 3.9+**
2. **Tushare Token** - 在 `.env` 文件中配置

## ⚙️ 安装

```bash
# 1. 克隆项目
git clone <repository-url>
cd shannon-stock-analyzer

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置Token
# 复制 .env.example 到 .env
# 编辑 .env，添加你的 Tushare Token
TUSHARE_TOKEN=your_token_here
```

## 🎯 使用方法

### 方法1: 全自动扫描（推荐）

```bash
run_scan.bat
```

这会自动：
1. 下载全市场数据（5000+只股票，180天）
2. 扫描Shannon候选
3. 导出结果到 `results/` 文件夹

### 方法2: 分步执行

```bash
# 步骤1: 下载数据
python scripts/download/download_all_stocks.py

# 步骤2: 扫描分析
python scripts/find_all_shannon.py
```

### 方法3: 快速测试（24只股票）

```bash
python scripts/find_shannon_with_ichimoku.py
```

## 📊 查看结果

结果保存在 `results/` 文件夹：
- `all_shannon_*.csv` - 全部候选
- `super_shannon_*.csv` - 超级信号（>=80分）
- `tech_shannon_*.csv` - 科技股候选

## 🔧 定时任务

在22:00自动运行：

```bash
# Windows
tools/run_at_22pm.bat

# Python
python tools/schedule_scan.py --time 22:00
```

## 📖 更多文档

- [完整指南](docs/ULTIMATE_SCAN_GUIDE.md)
- [Shannon标准](docs/SHANNON_CRITERIA.md)
- [Ichimoku分析](docs/ICHIMOKU_RESULTS.md)
- [贡献指南](CONTRIBUTING.md)

## ⚠️ 注意事项

- Tushare API有频率限制（每小时1次）
- 首次下载需要30-40分钟
- 确保有足够磁盘空间（>2GB）

## 🎉 最新结果

**超级信号（88分）**:
- 688005 (容百科技) - Ichimoku强势 + MCDX金叉 + 成交量达标

**强烈推荐（70-78分）**:
- 002812 (恩捷股份)
- 002466 (天齐锂业)
- 002460 (赣锋锂业)

---

**开始寻找下一个Shannon！** 🚀
