# Quick Start Guide - 快速开始指南

## English

### Installation & Setup

1. **Install Python 3.7+** from [python.org](https://python.org)

2. **Clone/Download this repository**

3. **Run the installer** (Choose one):
   - **Windows**: Double-click `install.bat`
   - **macOS/Linux**: Run `bash install.sh` in terminal

4. **Start the application** (Choose one):
   - **Windows**: Double-click `run.bat`
   - **macOS/Linux**: Run `python main.py` in terminal

### First Steps

1. **Create a reminder**:
   - Click "+ Add Reminder" button
   - Enter reminder title, date, time, priority
   - Click Save

2. **Create a custom list**:
   - Click "+ New List" in the left sidebar
   - Enter list name and choose color
   - Click Save

3. **Manage reminders**:
   - Right-click on a reminder for options
   - Double-click to edit
   - Click on different lists to filter

4. **Switch theme**:
   - Go to View menu → Dark Mode
   - Choose between light and dark themes

5. **Change language**:
   - Go to View menu → Language
   - Select English or 中文

---

## 中文

### 安装和设置

1. **安装Python 3.7+** 从 [python.org](https://python.org)

2. **克隆或下载此仓库**

3. **运行安装程序** (选择一个):
   - **Windows**: 双击 `install.bat`
   - **macOS/Linux**: 在终端运行 `bash install.sh`

4. **启动应用程序** (选择一个):
   - **Windows**: 双击 `run.bat`
   - **macOS/Linux**: 在终端运行 `python main.py`

### 开始使用

1. **创建提醒**:
   - 点击 "+ 添加提醒" 按钮
   - 输入提醒标题、日期、时间和优先级
   - 点击保存

2. **创建自定义列表**:
   - 点击左侧边栏的 "+ 新列表"
   - 输入列表名称并选择颜色
   - 点击保存

3. **管理提醒**:
   - 右键点击提醒查看选项
   - 双击编辑提醒
   - 点击不同列表来过滤

4. **切换主题**:
   - 进入 View 菜单 → Dark Mode
   - 在浅色和深色主题之间选择

5. **切换语言**:
   - 进入 View 菜单 → Language
   - 选择 English 或 中文

---

## Troubleshooting / 故障排除

### Problem: "ModuleNotFoundError: No module named 'PyQt5'"
**Solution**: Make sure you ran the installer (`install.bat` or `install.sh`) before starting the app.

### Problem: Application won't start
**Solution**: 
1. Make sure Python 3.7+ is installed and in your PATH
2. Delete the `venv` folder and re-run the installer
3. Check that PyQt5 is installed: `pip list | grep PyQt5`

### Problem: Data not saving
**Solution**: 
- Check that you have write permission to the application folder
- Make sure the `data` folder can be created
- Try running as administrator (Windows) or with sudo (macOS/Linux)

---

## System Requirements / 系统要求

- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)
- **Python**: 3.7 or higher
- **RAM**: 256 MB minimum
- **Storage**: 50 MB for installation

---

## Support / 支持

For more information, see [README.md](README.md)

有更多问题？请参考 [README.md](README.md)
