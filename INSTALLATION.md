# 安装和使用指南 - Installation & Usage Guide

## 项目概览 / Project Overview

**Reminders** 是一个受iOS原生提醒事项应用启发的现代桌面应用。它用Python和PyQt5构建，提供深浅色主题支持和多语言界面。

**Reminders** is a modern desktop application inspired by the native iOS Reminders app. Built with Python and PyQt5, it offers dark/light theme support and multi-language interface.

---

## 系统要求 / System Requirements

| 要求 | 最低版本 | 建议版本 |
|------|---------|---------|
| Python | 3.7+ | 3.9+ |
| RAM | 256 MB | 512 MB |
| 硬盘 | 100 MB | 200 MB |
| OS | Windows 7 / macOS 10.12 / Linux | Windows 10 / macOS 11 / Linux (latest) |

---

## 快速安装 / Quick Installation

### Windows

1. **安装Python** - 从 [python.org](https://python.org) 下载并安装（勾选 "Add Python to PATH"）

2. **下载项目** - 克隆或下载本项目到本地

3. **安装依赖** - 双击 `install.bat` 或在命令行运行：
   ```batch
   install.bat
   ```

4. **启动应用** - 双击 `run.bat` 或运行：
   ```batch
   python main.py
   ```

### macOS / Linux

1. **安装Python** - 运行：
   ```bash
   # macOS
   brew install python3
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install python3 python3-pip
   ```

2. **下载项目** - 克隆或下载本项目到本地

3. **安装依赖** - 运行：
   ```bash
   bash install.sh
   ```
   或手动安装：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **启动应用** - 运行：
   ```bash
   python3 main.py
   ```

---

## 详细使用指南 / Detailed Usage Guide

### 1. 创建提醒 / Creating Reminders

```
步骤 / Steps:
1. 点击 "+ Add Reminder" / Click "+ Add Reminder" button
2. 填写以下字段 / Fill in the following:
   - Title (标题) - 必填 / Required
   - List (列表) - 选择所属列表
   - Notes (备注) - 可选 / Optional
   - Due Date (完成日期) - 设置日期
   - Due Time (完成时间) - 非全天时显示
   - All-day (全天) - 复选框
   - Priority (优先级) - 选择 High/Medium/Low/None
   - Repeat (重复) - 每天/周/月/年
   - Alert (提醒) - 提前15分钟/1小时/1天
3. 点击 Save / Click Save
```

### 2. 管理提醒 / Managing Reminders

**右键菜单选项 / Right-click Options:**
- ☑ Mark Complete - 标记为完成
- 🚩 Flag - 标记为重要
- 🗑 Delete - 删除提醒

**其他操作 / Other Actions:**
- 双击提醒 - 编辑详情
- 点击智能列表 - 过滤显示
  - Today - 今天的提醒
  - Scheduled - 有计划的提醒
  - All - 所有未完成提醒
  - Flagged - 标记的提醒

### 3. 管理列表 / Managing Lists

```
创建新列表 / Create List:
1. 点击左侧 "+ New List" / Click "+ New List"
2. 输入列表名称 / Enter list name
3. 选择颜色 / Choose color
4. 点击 Save / Click Save

编辑列表 / Edit List:
1. 右键点击列表
2. 编辑或删除
```

### 4. 切换主题 / Switching Themes

```
菜单路径 / Menu Path:
View (视图) → Dark Mode (深色模式)

效果 / Effects:
- Light Mode: 清爽、专业的外观 / Clean, professional appearance
- Dark Mode: 护眼、夜间友好 / Eye-friendly, night-friendly
```

### 5. 切换语言 / Changing Language

```
菜单路径 / Menu Path:
View (视图) → Language (语言)

可用语言 / Available Languages:
- English (英文)
- 中文 (简体中文)

UI会立即更新 / UI updates immediately
```

---

## 数据存储位置 / Data Storage Locations

| 数据类型 | 位置 | 格式 |
|---------|------|------|
| 提醒 | `data/reminders.json` | JSON |
| 列表 | `data/lists.json` | JSON |
| 配置 | `~/.reminders-app/config.json` | JSON |

---

## 键盘快捷键 / Keyboard Shortcuts

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建提醒 |
| Ctrl+Q | 退出应用 |
| Delete | 删除选定提醒 |
| Enter | 编辑选定提醒 |

---

## 常见问题 / FAQ

### Q: 应用不能启动

**A:** 尝试以下方法：
1. 确保Python 3.7+已安装：`python --version`
2. 重新安装依赖：`pip install -r requirements.txt`
3. 删除`venv`文件夹，重新运行`install.bat`/`install.sh`
4. 以管理员身份运行应用

### Q: 提醒数据在哪里保存？

**A:** 数据保存在两个地方：
- 提醒文件：`项目目录/data/reminders.json`
- 配置文件：`用户主目录/.reminders-app/config.json`

### Q: 如何导出我的提醒？

**A:** 直接复制 `data/reminders.json` 文件。这是标准JSON格式，可以用任何文本编辑器打开。

### Q: 可以同步到手机吗？

**A:** 当前版本仅提供本地存储。云同步功能计划在v2.0中实现。

### Q: 如何重置应用设置？

**A:** 删除 `~/.reminders-app/config.json` 文件将重置所有设置为默认值。

### Q: 支持哪些语言？

**A:** 当前支持：
- 英文 (English)
- 简体中文 (Simplified Chinese)

更多语言正在计划中。

---

## 故障排除 / Troubleshooting

### 问题：Windows中"找不到模块PyQt5"

```
解决方案 Solution:
1. 打开命令提示符 (CMD)
2. 运行：pip install --upgrade PyQt5
3. 重新启动应用
```

### 问题：应用响应缓慢

```
解决方案 Solution:
1. 关闭其他应用确保有足够内存
2. 检查是否有大量提醒（超过10000条）
3. 重新启动应用
```

### 问题：主题切换不生效

```
解决方案 Solution:
1. 确认PyQt5版本正确：pip show PyQt5
2. 重新启动应用
3. 删除 ~/.reminders-app/config.json 并重启
```

### 问题：语言切换后显示混乱

```
解决方案 Solution:
1. 关闭并重新启动应用
2. 清除 ~/.reminders-app/config.json
3. 重新选择语言
```

---

## 性能优化 / Performance Tips

1. **减少内存占用**：
   - 定期删除已完成的提醒
   - 控制列表数量（建议< 50个）

2. **加快启动速度**：
   - 关闭系统中的其他应用
   - 升级到最新Python版本

3. **提高响应速度**：
   - 确保SSD有足够空间
   - 定期清理系统缓存

---

## 文件结构解释 / File Structure Explanation

```
Memo-DeskApp/
├── main.py                  # 应用入口 / App entry point
├── requirements.txt         # Python依赖 / Dependencies
├── src/                     # 源代码 / Source code
│   ├── config.py           # 配置管理 / Config management
│   ├── core/               # 核心逻辑 / Business logic
│   │   └── reminder.py     # 数据模型 / Data models
│   ├── ui/                 # 用户界面 / User interface
│   │   ├── main_window.py  # 主窗口 / Main window
│   │   ├── dialogs.py      # 对话框 / Dialogs
│   │   └── themes.py       # 主题系统 / Theme system
│   └── i18n/               # 国际化 / Internationalization
│       └── translations.py # 翻译文本 / Translations
├── data/                   # 数据目录 / Data directory
│   ├── reminders.json      # 提醒数据 / Reminders
│   └── lists.json          # 列表数据 / Lists
├── README.md               # 项目文档 / Project docs
├── QUICKSTART.md           # 快速开始 / Quick start
└── PROJECT_SUMMARY.md      # 项目总结 / Project summary
```

---

## 开发和贡献 / Development & Contributing

### 设置开发环境 / Setup Dev Environment

```bash
# 克隆项目
git clone <repository-url>
cd Memo-DeskApp

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# （可选）安装开发工具
pip install pylint flake8 black
```

### 代码风格 / Code Style

- 遵循 PEP 8
- 使用类型提示
- 添加文档字符串

### 提交代码 / Code Submission

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证 / License

本项目开源提供，可自由用于个人和商业用途。

This project is open source and available for personal and commercial use.

---

## 支持 / Support

- 📖 查看完整文档：[README.md](README.md)
- 🚀 快速开始指南：[QUICKSTART.md](QUICKSTART.md)
- 📝 项目总结：[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

For more help, check the documentation files above.

---

**最后更新** / Last Updated: 2024-03-01
**版本** / Version: 1.0.0
