"""
项目清理和最终整理
删除无用文件，整理文件夹结构
"""

import os
import shutil
from pathlib import Path

# 要删除的文件（无用或重复）
FILES_TO_DELETE = [
    # 旧的Pine Script文件（已集成到代码中）
    'mcdx_plus.pine',

    # 重复的环境配置文件
    '.env.example',  # 保留一个在根目录

    # 临时重组脚本
    'REORGANIZE_PROJECT.py',

    # 旧的主程序（功能已被新脚本替代）
    'main.py',

    # PowerShell安装脚本（不常用）
    'install.ps1',
]

# 要移动到tools文件夹的工具脚本
TOOLS_SCRIPTS = [
    'schedule_scan.py',
    'schedule_scan_22pm.bat',
    'run_at_22pm.bat',
]

# 要移动到根目录的重要文档
ROOT_DOCS = [
    'docs/AUTO_SCAN_README.md',  # 重命名为 QUICKSTART.md
    'docs/SHANNON_CRITERIA.md',
]


def create_folders():
    """创建必要的文件夹"""
    folders = [
        'tools',           # 工具脚本
        'examples',        # 示例代码
        '.github',         # GitHub配置
    ]

    print("=" * 80)
    print("创建文件夹")
    print("=" * 80)

    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✓ {folder}/")


def delete_files():
    """删除无用文件"""
    print("\n" + "=" * 80)
    print("删除无用文件")
    print("=" * 80)

    deleted = 0
    for file in FILES_TO_DELETE:
        file_path = Path(file)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ 删除: {file}")
            deleted += 1
        else:
            print(f"○ 不存在: {file}")

    print(f"\n删除了 {deleted} 个文件")


def move_tools():
    """移动工具脚本"""
    print("\n" + "=" * 80)
    print("移动工具脚本到 tools/")
    print("=" * 80)

    moved = 0
    for file in TOOLS_SCRIPTS:
        src = Path(file)
        if src.exists():
            dst = Path('tools') / src.name
            shutil.move(str(src), str(dst))
            print(f"✓ 移动: {file} -> tools/")
            moved += 1

    print(f"\n移动了 {moved} 个文件")


def create_quickstart():
    """创建快速开始文档"""
    print("\n" + "=" * 80)
    print("创建 QUICKSTART.md")
    print("=" * 80)

    quickstart = """# 🚀 快速开始

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
"""

    with open('QUICKSTART.md', 'w', encoding='utf-8') as f:
        f.write(quickstart)

    print("✓ 创建 QUICKSTART.md")


def create_github_workflow():
    """创建GitHub Actions工作流"""
    print("\n" + "=" * 80)
    print("创建 GitHub Actions 配置")
    print("=" * 80)

    workflow = """name: Python Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test imports
      run: |
        python -c "from src.mcdx.calculator import MCDXCalculator"
        python -c "from src.indicators.ichimoku import IchimokuCalculator"
"""

    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)

    with open(workflow_dir / 'python-tests.yml', 'w', encoding='utf-8') as f:
        f.write(workflow)

    print("✓ 创建 .github/workflows/python-tests.yml")


def update_readme():
    """更新README，添加项目结构"""
    print("\n" + "=" * 80)
    print("更新 README.md")
    print("=" * 80)

    # 读取现有README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 添加徽章
    badges = """
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

"""

    # 在标题后插入徽章
    if '[![' not in content:
        content = content.replace('# Shannon Stock Analyzer\n',
                                  '# Shannon Stock Analyzer\n' + badges)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ 更新 README.md")


def create_example():
    """创建示例代码"""
    print("\n" + "=" * 80)
    print("创建示例代码")
    print("=" * 80)

    example = """\"\"\"
Shannon Stock Analyzer - 使用示例
\"\"\"

from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mcdx.calculator import MCDXCalculator
from src.indicators.ichimoku import IchimokuCalculator
import pandas as pd

def example_mcdx():
    \"\"\"MCDX分析示例\"\"\"
    print("=" * 80)
    print("MCDX分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # 计算MCDX
    calc = MCDXCalculator()
    result = calc.calculate(df, '688005')
    
    print(f"\\n股票: 688005")
    print(f"Profit Chips: {result.profit_chips:.1f}%")
    print(f"SMA PC: {result.sma_profit_chips:.1f}%")
    print(f"Locked Chips: {result.locked_chips:.1f}%")
    print(f"行为: {result.behavior}")
    print(f"建议: {result.recommendation}")

def example_ichimoku():
    \"\"\"Ichimoku分析示例\"\"\"
    print("\\n" + "=" * 80)
    print("Ichimoku分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # 计算Ichimoku
    calc = IchimokuCalculator()
    result = calc.calculate(df)
    
    print(f"\\n股票: 688005")
    print(f"云层颜色: {result.cloud_color}")
    print(f"价格位置: {result.price_vs_cloud}")
    print(f"强烈看涨: {result.strong_bullish}")
    print(f"Ichimoku评分: {result.ichimoku_score:.0f}/100")
    print(f"信号: {calc.get_signal_description(result)}")

def example_combined():
    \"\"\"综合分析示例\"\"\"
    print("\\n" + "=" * 80)
    print("综合分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # MCDX
    mcdx_calc = MCDXCalculator()
    mcdx_result = mcdx_calc.calculate(df, '688005')
    
    # Ichimoku
    ichimoku_calc = IchimokuCalculator()
    ichimoku_result = ichimoku_calc.calculate(df)
    
    # 综合评分
    mcdx_score = 0
    if mcdx_result.profit_chips >= 80:
        mcdx_score += 20
    if mcdx_result.sma_profit_chips >= 85:
        mcdx_score += 15
    if mcdx_result.locked_chips < 15:
        mcdx_score += 5
    
    ichimoku_score = ichimoku_result.ichimoku_score * 0.3
    
    total_score = mcdx_score + ichimoku_score
    
    print(f"\\n股票: 688005 (容百科技)")
    print(f"MCDX评分: {mcdx_score}/40")
    print(f"Ichimoku评分: {ichimoku_score:.0f}/30")
    print(f"总分: {total_score:.0f}/70")
    
    if total_score >= 60:
        print("\\n评级: 🔥🔥 强烈推荐")
    elif total_score >= 40:
        print("\\n评级: 🔥 值得关注")
    else:
        print("\\n评级: ❌ 不符合")

if __name__ == '__main__':
    example_mcdx()
    example_ichimoku()
    example_combined()
"""

    with open('examples/basic_usage.py', 'w', encoding='utf-8') as f:
        f.write(example)

    print("✓ 创建 examples/basic_usage.py")


def print_final_structure():
    """打印最终项目结构"""
    print("\n" + "=" * 80)
    print("最终项目结构")
    print("=" * 80)

    structure = """
shannon-stock-analyzer/
├── README.md                   # 项目说明
├── QUICKSTART.md              # 快速开始
├── CONTRIBUTING.md            # 贡献指南
├── LICENSE                    # 许可证
├── requirements.txt           # 依赖列表
├── .gitignore                # Git忽略文件
├── .env.example              # 环境变量示例
├── run_scan.bat              # 一键运行脚本
│
├── src/                      # 核心代码
│   ├── __init__.py
│   ├── mcdx/                # MCDX计算器
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   └── volume_analyzer.py
│   ├── indicators/          # 技术指标
│   │   ├── __init__.py
│   │   └── ichimoku.py
│   └── data/                # 数据加载器
│       ├── __init__.py
│       ├── china_stock_api.py
│       ├── local_data_loader.py
│       ├── folder_data_loader.py
│       └── tdx_data_loader.py
│
├── scripts/                 # 分析脚本
│   ├── find_all_shannon.py          # 全市场扫描
│   ├── find_shannon_with_ichimoku.py # 24只股票分析
│   ├── find_next_shannon_24.py      # Shannon候选分析
│   ├── find_golden_cross.py         # 金叉检测
│   ├── download/                    # 数据下载
│   │   ├── download_all_stocks.py
│   │   └── download_tushare.py
│   ├── automation/                  # 自动化
│   │   └── auto_scan_complete.py
│   ├── test/                        # 测试脚本
│   └── legacy/                      # 旧版本（保留）
│
├── batch/                   # Windows批处理
│   ├── RUN_AUTO_SCAN.bat
│   ├── FIND_ALL_SHANNON.bat
│   └── ...
│
├── tools/                   # 工具脚本
│   ├── schedule_scan.py
│   └── run_at_22pm.bat
│
├── docs/                    # 文档
│   ├── ULTIMATE_SCAN_GUIDE.md
│   ├── SHANNON_CRITERIA.md
│   ├── ICHIMOKU_RESULTS.md
│   └── legacy/              # 旧文档
│
├── config/                  # 配置文件
│   ├── config.yaml
│   └── config_tech_focus.yaml
│
├── examples/                # 示例代码
│   └── basic_usage.py
│
├── .github/                 # GitHub配置
│   └── workflows/
│       └── python-tests.yml
│
├── results/                 # 分析结果（.gitignore）
└── data/                    # 数据文件（.gitignore）
"""

    print(structure)


def main():
    """主函数"""
    print("=" * 80)
    print("Shannon Stock Analyzer - 项目清理")
    print("=" * 80)
    print()

    # 1. 创建文件夹
    create_folders()

    # 2. 删除无用文件
    delete_files()

    # 3. 移动工具脚本
    move_tools()

    # 4. 创建快速开始文档
    create_quickstart()

    # 5. 创建GitHub Actions
    create_github_workflow()

    # 6. 更新README
    update_readme()

    # 7. 创建示例代码
    create_example()

    # 8. 打印最终结构
    print_final_structure()

    print("\n" + "=" * 80)
    print("✓ 项目清理完成！")
    print("=" * 80)
    print()
    print("项目已整理完毕，可以推送到GitHub了！")
    print()
    print("下一步:")
    print("  1. 查看 QUICKSTART.md")
    print("  2. 测试运行: run_scan.bat")
    print("  3. 提交到Git: git add . && git commit -m 'Initial commit'")
    print()


if __name__ == '__main__':
    main()
