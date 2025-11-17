# Troubleshooting Guide

## 🔧 Common Errors and Solutions

### Error: "ModuleNotFoundError: No module named 'xxx'"

**Problem**: Required Python packages are not installed.

**Solution**:

1. **Install all dependencies at once** (Recommended):

   ```bash
   pip install -r requirements.txt
   ```

2. **Or use the installation script** (Windows):

   ```bash
   install_dependencies.bat
   ```

3. **Or install individually**:
   ```bash
   pip install pandas numpy requests PyYAML python-dotenv akshare
   ```

### Error: "ImportError: cannot import name 'xxx'"

**Problem**: Package version mismatch or corrupted installation.

**Solution**:

1. Upgrade pip:

   ```bash
   python -m pip install --upgrade pip
   ```

2. Reinstall the problematic package:
   ```bash
   pip uninstall <package_name>
   pip install <package_name>
   ```

### Error: "No module named 'yaml'"

**Problem**: PyYAML package is installed but imported as 'yaml'.

**Solution**:

```bash
pip install PyYAML
```

### Error: "No module named 'dotenv'"

**Problem**: python-dotenv package is installed but imported as 'dotenv'.

**Solution**:

```bash
pip install python-dotenv
```

### Error: "akshare" related errors

**Problem**: AKShare package issues or network problems.

**Solutions**:

1. **Install/Reinstall AKShare**:

   ```bash
   pip install akshare --upgrade
   ```

2. **Check internet connection**: AKShare needs internet to fetch data.

3. **Try alternative data source**: Edit `config.yaml`:
   ```yaml
   stocks:
     china_data_source: "tushare" # or "ths"
   ```

### Error: "Permission denied" or "Access denied"

**Problem**: Insufficient permissions to install packages.

**Solution**:

1. **Run as administrator** (Windows):

   - Right-click Command Prompt
   - Select "Run as administrator"
   - Run installation command

2. **Use --user flag**:
   ```bash
   pip install --user -r requirements.txt
   ```

### Error: "pip is not recognized"

**Problem**: pip is not in system PATH.

**Solution**:

1. **Use python -m pip**:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Add Python to PATH**:
   - Windows: Add `C:\Python3x\Scripts` to PATH
   - Or reinstall Python with "Add to PATH" option

## 🔍 Diagnostic Tools

### 1. Run System Diagnostic

```bash
python diagnose.py
```

This will check:

- ✅ Python version
- ✅ Pip installation
- ✅ File structure
- ✅ Environment configuration
- ✅ Package installation

### 2. Run Simple Test

```bash
python test_simple.py
```

This will:

- ✅ Test package imports
- ✅ Test basic functionality
- ✅ Provide installation instructions if needed

### 3. Run Full Test

```bash
python test_china_mcdx.py
```

This will:

- ✅ Fetch real stock data
- ✅ Calculate MCDX indicators
- ✅ Display analysis results

## 📋 Step-by-Step Setup

### For Complete Beginners

1. **Check Python installation**:

   ```bash
   python --version
   ```

   Should show Python 3.8 or higher.

2. **Run diagnostic**:

   ```bash
   python diagnose.py
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or on Windows:

   ```bash
   install_dependencies.bat
   ```

4. **Configure credentials**:

   - Open `.env` file
   - Replace `your_app_id_here` with your actual appId
   - Replace `your_app_key_here` with your actual appKey
   - Get credentials from: https://aimiai.com/console

5. **Run simple test**:

   ```bash
   python test_simple.py
   ```

6. **Run full test**:
   ```bash
   python test_china_mcdx.py
   ```

## 🌐 Network Issues

### Problem: "Connection timeout" or "Network error"

**Solutions**:

1. **Check internet connection**

2. **Use proxy** (if behind firewall):

   ```bash
   set HTTP_PROXY=http://proxy.example.com:8080
   set HTTPS_PROXY=http://proxy.example.com:8080
   pip install -r requirements.txt
   ```

3. **Use mirror** (China users):
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

## 🐛 Still Having Issues?

### Collect Information

Run these commands and save the output:

```bash
python --version
pip --version
python diagnose.py
```

### Check Specific Files

1. **Verify file exists**:

   ```bash
   dir src\data\china_stock_api.py
   dir src\mcdx\calculator.py
   ```

2. **Check Python path**:

   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   ```

3. **List installed packages**:
   ```bash
   pip list
   ```

## 💡 Quick Fixes

### "It was working before, now it's broken"

1. **Reinstall dependencies**:

   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

2. **Clear Python cache**:
   ```bash
   python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
   ```

### "I just want to test if it works"

Run the minimal test:

```bash
python test_simple.py
```

This requires only basic packages and will tell you exactly what's missing.

## 📞 Getting Help

If you're still stuck:

1. Run `python diagnose.py` and save the output
2. Note the exact error message
3. Check which step fails:
   - Installation?
   - Import?
   - Data fetching?
   - MCDX calculation?

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] All packages installed (`pip list` shows them)
- [ ] `.env` file configured with real credentials
- [ ] `python test_simple.py` passes
- [ ] `python test_china_mcdx.py` runs successfully

Once all items are checked, you're ready to use the analyzer! 🎉
