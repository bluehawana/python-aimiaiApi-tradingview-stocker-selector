# 🚀 Quick Fix - Python 3.9 Installation

## 问题诊断

你的系统：

- ✅ Python 3.9.13 (兼容)
- ❌ pandas-ta 包不可用（不需要，我们有自定义 MCDX）
- ❌ 某些包版本不兼容 Python 3.9

## 🔧 解决方案

### 方法 1：使用 PowerShell 脚本（推荐）

```powershell
.\install.ps1
```

### 方法 2：使用批处理脚本

```cmd
install_step_by_step.bat
```

### 方法 3：手动安装（逐个安装）

```powershell
# 1. 升级 pip
python -m pip install --upgrade pip

# 2. 安装核心包
pip install numpy==1.24.4
pip install pandas==1.5.3

# 3. 安装其他包
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install PyYAML==6.0.1

# 4. 安装中国股市数据包
pip install akshare==1.11.84

# 5. 验证安装
python diagnose.py
```

### 方法 4：使用最小化 requirements

```powershell
pip install -r requirements_minimal.txt
```

## ✅ 验证安装

安装完成后运行：

```powershell
python test_simple.py
```

应该看到：

```
✅ pandas          - Data processing
✅ numpy           - Numerical computing
✅ requests        - HTTP client
✅ yaml            - YAML parser
✅ dotenv          - Environment variables
✅ akshare         - China stock data
```

## 🎯 下一步

安装成功后：

```powershell
# 测试中国股市数据和 MCDX
python test_china_mcdx.py
```

## 📝 注意事项

1. **pandas-ta 不需要** - 我们有自定义的 MCDX 计算器
2. **Flask 暂时不需要** - 先测试核心功能
3. **tushare 可选** - akshare 已经足够

## ❓ 还是有问题？

运行诊断：

```powershell
python diagnose.py
```

这会告诉你具体哪里有问题。
