# Shannon Stock Analyzer - 项目总结

## 🎯 项目概述

专业的 A 股技术分析系统，结合 MCDX（筹码分布）、Ichimoku Cloud（一目均衡表）和成交量分析，自动扫描全市场寻找下一个 Shannon。

## ✨ 核心功能

### 1. 三重技术分析

- **MCDX 分析** (40 分) - 筹码分布金叉检测
- **Ichimoku Cloud** (30 分) - 云层突破信号
- **成交量分析** (20 分) - 成交量暴增检测
- **价格分析** (10 分) - 涨幅和趋势

### 2. 全市场扫描

- 支持 5000+只 A 股（上海+深圳）
- 180 天历史数据分析
- 智能筛选：金叉 + 评分>=40

### 3. 自动化运行

- 一键扫描全市场
- 定时任务支持
- 自动导出结果

## 📊 最新成果

### 超级信号 (88 分)

**688005 (容百科技)**

- Ichimoku 强势：价格突破云层，云层转为看涨 ✅
- MCDX 金叉：PC 95.3% ✅
- 成交量达标：2.50x ✅
- 价格涨幅：+19.8% ✅

### 强烈推荐 (70-78 分)

1. **002812 (恩捷股份)** - 78 分
2. **002466 (天齐锂业)** - 76 分
3. **002460 (赣锋锂业)** - 70 分

## 🏗️ 项目结构

```
shannon-stock-analyzer/
├── src/                    # 核心代码
│   ├── mcdx/              # MCDX计算器
│   ├── indicators/        # Ichimoku等指标
│   └── data/              # 数据加载器
├── scripts/               # 分析脚本
│   ├── find_all_shannon.py
│   ├── find_shannon_with_ichimoku.py
│   └── download/          # 数据下载
├── batch/                 # Windows批处理
├── tools/                 # 工具脚本
├── docs/                  # 文档
├── config/                # 配置文件
└── examples/              # 示例代码
```

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置Token
cp .env.example .env
# 编辑 .env，添加 TUSHARE_TOKEN

# 3. 运行扫描
run_scan.bat
```

## 📈 技术亮点

### 1. Ichimoku Cloud 集成

- 完整实现一目均衡表
- 自动识别云层突破
- 强烈看涨信号检测

### 2. MCDX 筹码分析

- 基于 Pine Script 移植
- 金叉/死叉检测
- 行为分析和建议

### 3. 智能评分系统

- 100 分综合评分
- 多维度分析
- 自动分级（超级/强烈/关注）

### 4. 全自动化

- 数据下载自动化
- 扫描分析自动化
- 结果导出自动化
- 定时任务支持

## 📚 文档完整性

- ✅ README.md - 项目说明
- ✅ QUICKSTART.md - 快速开始
- ✅ CONTRIBUTING.md - 贡献指南
- ✅ LICENSE - MIT 许可证
- ✅ docs/ - 完整文档
- ✅ examples/ - 示例代码

## 🔧 技术栈

- **Python 3.9+**
- **pandas** - 数据处理
- **numpy** - 数值计算
- **tushare** - 数据源
- **schedule** - 定时任务

## 📦 代码质量

- ✅ 模块化设计
- ✅ 类型注解
- ✅ 文档字符串
- ✅ 错误处理
- ✅ GitHub Actions CI

## 🎯 使用场景

### 1. 日常监控

每日运行扫描，寻找新的 Shannon 候选

### 2. 板块分析

按行业统计，发现热点板块

### 3. 技术研究

学习 MCDX 和 Ichimoku 指标

### 4. 量化策略

作为量化交易策略的一部分

## ⚠️ 免责声明

本工具仅供学习和研究使用，不构成投资建议。股市有风险，投资需谨慎。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**项目状态**: ✅ 生产就绪
**最后更新**: 2025-11-17
**版本**: 1.0.0

🚀 **寻找下一个 Shannon！**
