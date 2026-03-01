"""主题管理和样式系统"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict

class ThemeType(Enum):
    """主题类型"""
    LIGHT = 'light'
    DARK = 'dark'

@dataclass
class ColorScheme:
    """颜色方案"""
    # 基础颜色
    primary: str
    secondary: str
    background: str
    foreground: str
    
    # 边界和分隔符
    border: str
    separator: str
    
    # 状态颜色
    success: str
    warning: str
    error: str
    info: str
    
    # 文字颜色
    text_primary: str
    text_secondary: str
    text_tertiary: str
    
    # 背景变体
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    
    # 其他
    shadow: str
    hover_bg: str
    selected_bg: str

LIGHT_THEME = ColorScheme(
    primary='#007AFF',
    secondary='#5AC8FA',
    background='#FFFFFF',
    foreground='#F2F2F7',
    
    border='#E1E3E6',
    separator='#D1D1D6',
    
    success='#34C759',
    warning='#FF9500',
    error='#FF3B30',
    info='#007AFF',
    
    text_primary='#000000',
    text_secondary='#666666',
    text_tertiary='#999999',
    
    bg_primary='#FFFFFF',
    bg_secondary='#F2F2F7',
    bg_tertiary='#E8E8ED',
    
    shadow='rgba(0, 0, 0, 0.1)',
    hover_bg='#F0F0F5',
    selected_bg='#E8E8ED',
)

DARK_THEME = ColorScheme(
    primary='#0A84FF',
    secondary='#40B0FF',
    background='#1C1C1E',
    foreground='#2C2C2E',
    
    border='#3C3C3E',
    separator='#3E3E42',
    
    success='#30B0C0',
    warning='#FF9500',
    error='#FF453A',
    info='#0A84FF',
    
    text_primary='#FFFFFF',
    text_secondary='#999999',
    text_tertiary='#666666',
    
    bg_primary='#1C1C1E',
    bg_secondary='#2C2C2E',
    bg_tertiary='#3C3C3E',
    
    shadow='rgba(0, 0, 0, 0.3)',
    hover_bg='#3A3A3C',
    selected_bg='#44444E',
)

class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        """初始化主题管理器"""
        self.current_theme = ThemeType.LIGHT
        self.color_scheme = LIGHT_THEME
        self.theme_changed_callbacks = []
    
    def set_theme(self, theme_type: ThemeType):
        """设置主题
        
        Args:
            theme_type: 主题类型
        """
        if theme_type == ThemeType.LIGHT:
            self.color_scheme = LIGHT_THEME
        else:
            self.color_scheme = DARK_THEME
        
        self.current_theme = theme_type
        self._notify_theme_changed()
    
    def toggle_theme(self):
        """切换主题"""
        if self.current_theme == ThemeType.LIGHT:
            self.set_theme(ThemeType.DARK)
        else:
            self.set_theme(ThemeType.LIGHT)
    
    def is_dark_mode(self) -> bool:
        """检查是否为深色模式"""
        return self.current_theme == ThemeType.DARK
    
    def get_color(self, color_name: str) -> str:
        """获取颜色值"""
        return getattr(self.color_scheme, color_name, '#000000')
    
    def get_stylesheet(self) -> str:
        """获取应用样式表"""
        cs = self.color_scheme
        
        stylesheet = f"""
QMainWindow {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
}}

QWidget {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
}}

QListWidget, QTableWidget {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    border-radius: 8px;
}}

QListWidget::item, QTableWidget::item {{
    padding: 8px;
    border: none;
}}

QListWidget::item:hover, QTableWidget::item:hover {{
    background-color: {cs.hover_bg};
}}

QListWidget::item:selected, QTableWidget::item:selected {{
    background-color: {cs.primary};
    color: white;
}}

QPushButton {{
    background-color: {cs.primary};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {cs.secondary};
}}

QPushButton:pressed {{
    opacity: 0.8;
}}

QLineEdit, QTextEdit {{
    background-color: {cs.bg_secondary};
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    border-radius: 6px;
    padding: 8px;
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 2px solid {cs.primary};
}}

QComboBox, QSpinBox, QDateEdit, QTimeEdit {{
    background-color: {cs.bg_secondary};
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    border-radius: 6px;
    padding: 6px;
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background-color: {cs.bg_secondary};
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    selection-background-color: {cs.primary};
}}

QLabel {{
    color: {cs.text_primary};
}}

QMenuBar {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
    border-bottom: 1px solid {cs.border};
}}

QMenuBar::item:selected {{
    background-color: {cs.hover_bg};
}}

QMenu {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    border-radius: 6px;
}}

QMenu::item:selected {{
    background-color: {cs.primary};
    color: white;
}}

QCheckBox {{
    color: {cs.text_primary};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {cs.border};
    border-radius: 4px;
}}

QCheckBox::indicator:checked {{
    background-color: {cs.primary};
    border: 2px solid {cs.primary};
}}

QDialog {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
}}

QGroupBox {{
    color: {cs.text_primary};
    border: 1px solid {cs.border};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}

QFrame {{
    background-color: {cs.bg_primary};
    color: {cs.text_primary};
    border: none;
}}

QScrollBar:vertical {{
    background-color: {cs.bg_secondary};
    width: 12px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {cs.border};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {cs.separator};
}}
        """
        
        return stylesheet.strip()
    
    def on_theme_changed(self, callback):
        """注册主题改变回调"""
        self.theme_changed_callbacks.append(callback)
    
    def _notify_theme_changed(self):
        """通知主题已改变"""
        for callback in self.theme_changed_callbacks:
            callback()

# 全局主题管理器实例
_theme_manager = ThemeManager()

def get_theme_manager() -> ThemeManager:
    """获取主题管理器"""
    return _theme_manager
