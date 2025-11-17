# Shannon Pattern 快速参考

## 核心指标（2024 年 9 月 11-12 日案例）

### 📊 成交量指标

```
正常成交量：  30M
突破成交量：  89M
成交量比率：  3.0x (300%)
持续天数：    2天+
```

### 📈 MCDX 指标

```
红色柱状图 (Profit Chips):     100%
深红色线 (SMA Profit Chips):   86.65%
锁定筹码 (Locked Chips):       < 15%
```

## 筛选标准

| 指标             | 阈值    | 权重 |
| ---------------- | ------- | ---- |
| Profit Chips     | >= 80%  | 高   |
| SMA Profit Chips | >= 85%  | 高   |
| Locked Chips     | < 15%   | 中   |
| 成交量比率       | >= 2.5x | 高   |
| 成交量暴增       | 是      | 高   |
| 成交量趋势       | 上升    | 中   |
| 价格趋势         | 上升    | 高   |

## Shannon Score 分级

| 分数   | 等级   | 说明                             |
| ------ | ------ | -------------------------------- |
| 80-100 | 🔥🔥🔥 | 强烈推荐 - 极度接近 Shannon 模式 |
| 60-79  | 🔥🔥   | 值得关注 - 具有明显特征          |
| 40-59  | 🔥     | 观察 - 有潜力但需确认            |
| 0-39   | ❌     | 不符合 - 不符合 Shannon 模式     |

## 覆盖板块（9 大热门赛道）

1. **半导体芯片** - 中芯国际、北方华创、韦尔股份
2. **存储芯片** - 紫光国微、兆易创新、寒武纪
3. **CPO 光学** - 新易盛、中际旭创、光迅科技
4. **固态电池** - 宁德时代、国轩高科、赣锋锂业
5. **六氟磷酸锂** - 赣锋锂业、天齐锂业、亿纬锂能
6. **储能** - 宁德时代、固德威、锦浪科技
7. **光伏** - 隆基绿能、天合光能、晶澳科技
8. **智能电网** - 晶盛机电、先导智能
9. **机器人** - 机器人、石头科技、汇川技术

## 快速命令

```bash
# 基础扫描
python find_shannon_pattern.py

# 高标准扫描（分数 >= 70）
python find_shannon_pattern.py --min-score 70

# 导出结果
python find_shannon_pattern.py --export results/shannon.csv

# 测试设置
python test_shannon_setup.py
```

## API 认证

```bash
# .env 文件配置
AppId=你的_app_id
AppKey=你的_app_key
token=你的_token  # 可选，如果已有 token

# 获取 Token (POST 请求)
POST https://aimiai.com/api/token/get
Content-Type: application/json

{
  "appId": "你的_app_id",
  "appKey": "你的_app_key"
}

# 使用 Token (业务接口)
Authorization: Bearer {token}  # 注意 Bearer 后有空格
```

## 技术信号

| 信号               | 含义                | 重要性 |
| ------------------ | ------------------- | ------ |
| 🔥 Shannon Pattern | 完整的 Shannon 模式 | 极高   |
| ✨ Golden Cross    | SMA PC 上穿 SMA LC  | 高     |
| 🐉 Double Dragon   | 双龙出海形态        | 高     |
| 🎣 Bottom Catch    | 底部反转信号        | 中     |

## 风险提示

⚠️ **重要**：

- 本工具仅供参考，不构成投资建议
- 历史模式不代表未来表现
- 股市有风险，投资需谨慎
- 请结合基本面分析和市场环境

---

**找到下一个 Shannon！** 🚀
