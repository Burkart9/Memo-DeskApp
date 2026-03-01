"""主应用窗口"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QSplitter, QMenu, QAction, QMessageBox, QStatusBar,
    QTabWidget, QFrame, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QDate, QTimer, QPoint
from PyQt5.QtGui import QFont, QColor, QIcon, QBrush, QPixmap
from datetime import datetime
import os

from ..i18n.translations import get_translator, set_language
from ..core.reminder import get_storage, Reminder, ReminderList, Priority
from ..ui.dialogs import ReminderDialog, ListDialog
from ..ui.themes import get_theme_manager, ThemeType

class ReminderItemWidget(QWidget):
    """提醒事项列表项小部件"""
    
    def __init__(self, reminder: Reminder, parent=None):
        super().__init__(parent)
        self.reminder = reminder
        self.initUI()
    
    def sizeHint(self):
        """返回小部件的尺寸提示"""
        return QSize(400, 70)
    
    def initUI(self):
        """初始化UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        
        # 优先级指示器
        if self.reminder.priority > 0:
            priority_label = QLabel('●')
            priority_colors = {
                1: QColor('#FF9500'),  # Low
                2: QColor('#FF6B6B'),  # Medium
                3: QColor('#FF3B30'),  # High
            }
            priority_label.setStyleSheet(
                f'color: {priority_colors[self.reminder.priority].name()};'
            )
            layout.addWidget(priority_label)
        
        # 标题和描述
        text_layout = QVBoxLayout()
        
        title = QLabel(self.reminder.title)
        title_font = QFont()
        title_font.setPointSize(11)
        if self.reminder.is_completed:
            title_font.setStrikeOut(True)
        title.setFont(title_font)
        text_layout.addWidget(title)
        
        # 显示日期和描述摘要
        info_text = ''
        if self.reminder.due_date:
            info_text += f"Due: {self.reminder.due_date} "
        if self.reminder.description:
            info_text += f"• {self.reminder.description[:50]}"
        
        if info_text:
            info_label = QLabel(info_text)
            info_label.setStyleSheet('color: gray; font-size: 10px;')
            text_layout.addWidget(info_label)
        
        layout.addLayout(text_layout, 1)
        
        # 标记按钮
        if self.reminder.is_flagged:
            flag_label = QLabel('🚩')
            layout.addWidget(flag_label)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """主应用窗口"""
    
    def __init__(self):
        super().__init__()
        self.translator = get_translator()
        self.theme_manager = get_theme_manager()
        self.storage = get_storage()
        
        self.current_list_id = None
        self.current_filter = 'all'  # all, today, scheduled, flagged
        
        self.initUI()
        self.setup_connections()
        self.load_reminders()
        self.apply_theme()
    
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle(self.translator.get('app_title'))
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中央小部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # 左侧边栏 - 列表导航
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 右侧主要内容
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 3)
        
        central_widget.setLayout(main_layout)
        
        # 菜单栏
        self.create_menu_bar()
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # 标题
        title = QLabel(self.translator.get('app_title'))
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 智能列表
        smart_label = QLabel('SMART LISTS')
        smart_label.setStyleSheet('font-weight: bold; font-size: 11px; color: gray;')
        layout.addWidget(smart_label)
        
        self.smart_lists = {
            'today': self.translator.get('today'),
            'scheduled': self.translator.get('scheduled'),
            'all': self.translator.get('all'),
            'flagged': self.translator.get('flagged'),
        }
        
        self.smart_list_buttons = {}
        for list_id, list_name in self.smart_lists.items():
            btn = QPushButton(list_name)
            btn.setFlat(True)
            btn.clicked.connect(lambda checked, lid=list_id: self.select_smart_list(lid))
            self.smart_list_buttons[list_id] = btn
            layout.addWidget(btn)
        
        # 自定义列表
        custom_label = QLabel('MY LISTS')
        custom_label.setStyleSheet('font-weight: bold; font-size: 11px; color: gray;')
        layout.addWidget(custom_label)
        
        self.custom_lists_layout = QVBoxLayout()
        layout.addLayout(self.custom_lists_layout)
        
        # 新建列表按钮
        new_list_btn = QPushButton(f'+ {self.translator.get("new_list")}')
        new_list_btn.setFlat(True)
        new_list_btn.clicked.connect(self.show_new_list_dialog)
        layout.addWidget(new_list_btn)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    def create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        
        # 当前列表标题
        self.list_title = QLabel(self.translator.get('today'))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.list_title.setFont(title_font)
        toolbar.addWidget(self.list_title)
        
        toolbar.addStretch()
        
        # 添加提醒按钮
        self.add_btn = QPushButton(f'+ {self.translator.get("add_reminder")}')
        self.add_btn.clicked.connect(self.show_new_reminder_dialog)
        toolbar.addWidget(self.add_btn)
        
        layout.addLayout(toolbar)
        
        # 提醒列表
        self.reminders_list = QListWidget()
        self.reminders_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.reminders_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.reminders_list.customContextMenuRequested.connect(self.show_reminder_context_menu)
        self.reminders_list.itemDoubleClicked.connect(self.on_reminder_double_clicked)
        layout.addWidget(self.reminders_list)
        
        # 空状态提示
        self.empty_label = QLabel()
        self.empty_label.setText(self.translator.get('add_first_reminder'))
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet('color: gray; font-size: 14px;')
        
        panel.setLayout(layout)
        return panel
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu(self.translator.get('file'))
        exit_action = QAction(self.translator.get('exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu(self.translator.get('edit'))
        new_reminder_action = QAction(self.translator.get('add_reminder'), self)
        new_reminder_action.triggered.connect(self.show_new_reminder_dialog)
        edit_menu.addAction(new_reminder_action)
        
        # 视图菜单
        view_menu = menubar.addMenu(self.translator.get('view'))
        
        # 语言子菜单
        language_menu = view_menu.addMenu(self.translator.get('language'))
        
        en_action = QAction('English', self)
        en_action.triggered.connect(lambda: self.change_language('en'))
        language_menu.addAction(en_action)
        
        zh_action = QAction('中文', self)
        zh_action.triggered.connect(lambda: self.change_language('zh'))
        language_menu.addAction(zh_action)
        
        view_menu.addSeparator()
        
        # 主题切换
        dark_mode_action = QAction(self.translator.get('dark_mode'), self)
        dark_mode_action.setCheckable(True)
        dark_mode_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(dark_mode_action)
    
    def setup_connections(self):
        """设置信号连接"""
        self.theme_manager.on_theme_changed(self.apply_theme)
    
    def select_smart_list(self, list_id: str):
        """选择智能列表"""
        self.current_list_id = None
        self.current_filter = list_id
        self.update_list_display()
        
        # 更新按钮样式
        for bid, btn in self.smart_list_buttons.items():
            if bid == list_id:
                btn.setStyleSheet('background-color: lightblue;')
            else:
                btn.setStyleSheet('')
    
    def update_custom_lists(self):
        """更新自定义列表显示"""
        # 清空现有项
        while self.custom_lists_layout.count():
            self.custom_lists_layout.takeAt(0).widget().deleteLater()
        
        # 添加自定义列表
        for reminder_list in self.storage.get_custom_lists():
            btn = QPushButton(reminder_list.name)
            btn.setFlat(True)
            btn.setStyleSheet(f'color: {reminder_list.color};')
            btn.clicked.connect(
                lambda checked, lid=reminder_list.id: self.select_custom_list(lid)
            )
            self.custom_lists_layout.addWidget(btn)
    
    def select_custom_list(self, list_id: str):
        """选择自定义列表"""
        self.current_list_id = list_id
        self.current_filter = None
        self.update_list_display()
    
    def update_list_display(self):
        """更新列表显示"""
        reminders = []
        
        if self.current_filter == 'today':
            reminders = self.storage.get_today_reminders()
            self.list_title.setText(self.translator.get('today'))
        elif self.current_filter == 'flagged':
            reminders = self.storage.get_flagged_reminders()
            self.list_title.setText(self.translator.get('flagged'))
        elif self.current_filter == 'scheduled':
            reminders = [r for r in self.storage.get_pending_reminders() 
                        if r.due_date]
            self.list_title.setText(self.translator.get('scheduled'))
        elif self.current_filter == 'all':
            reminders = self.storage.get_pending_reminders()
            self.list_title.setText(self.translator.get('all'))
        elif self.current_list_id:
            reminders = self.storage.get_reminders_by_list(self.current_list_id)
            reminder_list = self.storage.get_list(self.current_list_id)
            if reminder_list:
                self.list_title.setText(reminder_list.name)
        
        # 排序：按优先级降序，再按创建时间
        reminders.sort(
            key=lambda r: (-r.priority, r.created_at),
            reverse=True
        )
        
        self.reminders_list.clear()
        
        if not reminders:
            self.reminders_list.addItem(
                self.translator.get('add_first_reminder')
            )
            return
        
        for reminder in reminders:
            item = QListWidgetItem()
            item_widget = ReminderItemWidget(reminder)
            item.setSizeHint(item_widget.sizeHint())
            item.setData(Qt.UserRole, reminder.id)
            self.reminders_list.addItem(item)
            self.reminders_list.setItemWidget(item, item_widget)
    
    def show_new_reminder_dialog(self):
        """显示新建提醒对话框"""
        lists = self.storage.get_all_lists()
        dialog = ReminderDialog(self, reminder_data=None, lists=lists)
        dialog.reminder_saved.connect(self.on_reminder_saved)
        dialog.exec_()
    
    def show_new_list_dialog(self):
        """显示新建列表对话框"""
        dialog = ListDialog(self, list_data=None)
        dialog.list_saved.connect(self.on_list_saved)
        dialog.exec_()
    
    def on_reminder_saved(self, reminder_data):
        """处理提醒保存"""
        if hasattr(self, '_edit_reminder_id'):
            # 编辑模式
            self.storage.update_reminder(self._edit_reminder_id, **reminder_data)
            delattr(self, '_edit_reminder_id')
        else:
            # 新建模式
            self.storage.add_reminder(**reminder_data)
        
        self.update_list_display()
        self.status_bar.showMessage(self.translator.get('saved'), 2000)
    
    def on_list_saved(self, list_data):
        """处理列表保存"""
        if hasattr(self, '_edit_list_id'):
            # 编辑模式
            self.storage.update_list(self._edit_list_id, **list_data)
            delattr(self, '_edit_list_id')
        else:
            # 新建模式
            self.storage.add_list(**list_data)
        
        self.update_custom_lists()
        self.status_bar.showMessage(self.translator.get('created'), 2000)
    
    def on_reminder_double_clicked(self, item):
        """处理提醒双击"""
        reminder_id = item.data(Qt.UserRole)
        if reminder_id:
            reminder = self.storage.get_reminder(reminder_id)
            if reminder:
                self._edit_reminder_id = reminder_id
                lists = self.storage.get_all_lists()
                dialog = ReminderDialog(self, reminder_data=reminder.to_dict(), lists=lists)
                dialog.reminder_saved.connect(self.on_reminder_saved)
                dialog.exec_()
    
    def show_reminder_context_menu(self, position):
        """显示提醒上下文菜单"""
        item = self.reminders_list.itemAt(position)
        if not item:
            return
        
        reminder_id = item.data(Qt.UserRole)
        if not reminder_id:
            return
        
        reminder = self.storage.get_reminder(reminder_id)
        if not reminder:
            return
        
        menu = QMenu()
        
        # 标记完成
        complete_action = QAction(self.translator.get('mark_complete'), self)
        complete_action.triggered.connect(
            lambda: self.toggle_reminder_complete(reminder_id)
        )
        menu.addAction(complete_action)
        
        # 标记/取消标记
        flag_text = 'Unflag' if reminder.is_flagged else self.translator.get('flagged')
        flag_action = QAction(flag_text, self)
        flag_action.triggered.connect(
            lambda: self.toggle_reminder_flag(reminder_id)
        )
        menu.addAction(flag_action)
        
        menu.addSeparator()
        
        # 删除
        delete_action = QAction(self.translator.get('delete'), self)
        delete_action.triggered.connect(
            lambda: self.delete_reminder(reminder_id)
        )
        menu.addAction(delete_action)
        
        menu.exec_(self.reminders_list.mapToGlobal(position))
    
    def toggle_reminder_complete(self, reminder_id: str):
        """切换提醒完成状态"""
        reminder = self.storage.get_reminder(reminder_id)
        if reminder:
            self.storage.update_reminder(reminder_id, is_completed=not reminder.is_completed)
            self.update_list_display()
    
    def toggle_reminder_flag(self, reminder_id: str):
        """切换提醒标记状态"""
        reminder = self.storage.get_reminder(reminder_id)
        if reminder:
            self.storage.update_reminder(reminder_id, is_flagged=not reminder.is_flagged)
            self.update_list_display()
    
    def delete_reminder(self, reminder_id: str):
        """删除提醒"""
        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            self.translator.get('confirm_delete'),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.storage.delete_reminder(reminder_id)
            self.update_list_display()
            self.status_bar.showMessage(self.translator.get('deleted'), 2000)
    
    def change_language(self, language: str):
        """切换语言"""
        set_language(language)
        self.translator = get_translator()
        
        # 重新初始化UI
        self.setWindowTitle(self.translator.get('app_title'))
        self.update_list_display()
        self.update_custom_lists()
    
    def toggle_theme(self):
        """切换主题"""
        self.theme_manager.toggle_theme()
    
    def apply_theme(self):
        """应用主题"""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def load_reminders(self):
        """加载提醒"""
        self.update_custom_lists()
        self.select_smart_list('today')
