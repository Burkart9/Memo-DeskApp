"""Reminders 桌面应用主入口"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from pathlib import Path

from src.ui.main_window import MainWindow
from src.ui.themes import get_theme_manager, ThemeType
from src.core.reminder import get_storage
from src.i18n.translations import set_language

def main():
    """应用主函数"""
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 初始化存储（相对于应用目录）
    app_dir = Path(__file__).parent.parent
    data_dir = app_dir / 'data'
    get_storage(str(data_dir))
    
    # 设置默认语言
    set_language('en')
    
    # 初始化主题
    theme_manager = get_theme_manager()
    theme_manager.set_theme(ThemeType.LIGHT)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
