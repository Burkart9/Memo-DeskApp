"""提醒事项应用对话框和小部件"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QCheckBox, QPushButton, QTextEdit, QDateEdit,
    QTimeEdit, QGroupBox, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon
from datetime import datetime

from ..i18n.translations import get_translator
from ..core.reminder import Priority, Repeat

class ReminderDialog(QDialog):
    """提醒事项编辑对话框"""
    
    reminder_saved = pyqtSignal(dict)
    
    def __init__(self, parent=None, reminder_data=None, lists=None):
        """初始化对话框
        
        Args:
            parent: 父窗口
            reminder_data: 提醒数据（编辑模式）
            lists: 可用的列表
        """
        super().__init__(parent)
        self.reminder_data = reminder_data
        self.lists = lists or []
        self.translator = get_translator()
        self.is_edit_mode = reminder_data is not None
        
        self.initUI()
        self.load_reminder_data()
    
    def initUI(self):
        """初始化UI"""
        title = self.translator.get(
            'edit_reminder' if self.is_edit_mode else 'add_new_reminder'
        )
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 500, 600)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel(self.translator.get('reminder_title') + ':')
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Enter reminder title...')
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        
        # 列表
        list_label = QLabel(self.translator.get('new_list') + ':')
        self.list_combo = QComboBox()
        for reminder_list in self.lists:
            self.list_combo.addItem(reminder_list.name, reminder_list.id)
        layout.addWidget(list_label)
        layout.addWidget(self.list_combo)
        
        # 描述/备注
        notes_label = QLabel(self.translator.get('notes') + ':')
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText('Add notes...')
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_input)
        
        # 日期和时间组织
        date_group = QGroupBox(self.translator.get('due_date'))
        date_layout = QVBoxLayout()
        
        # 日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        
        # 全天选项
        self.all_day_check = QCheckBox(self.translator.get('all_day'))
        self.all_day_check.stateChanged.connect(self.on_all_day_changed)
        date_layout.addWidget(self.all_day_check)
        
        # 时间选择
        time_label = QLabel(self.translator.get('due_time') + ':')
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        date_layout.addWidget(time_label)
        date_layout.addWidget(self.time_edit)
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # 优先级和提醒
        options_group = QGroupBox(self.translator.get('priority'))
        options_layout = QVBoxLayout()
        
        # 优先级选择
        priority_label = QLabel(self.translator.get('priority') + ':')
        self.priority_combo = QComboBox()
        self.priority_combo.addItem(
            self.translator.get('no_priority'), Priority.NONE.value
        )
        self.priority_combo.addItem(
            self.translator.get('low'), Priority.LOW.value
        )
        self.priority_combo.addItem(
            self.translator.get('medium'), Priority.MEDIUM.value
        )
        self.priority_combo.addItem(
            self.translator.get('high'), Priority.HIGH.value
        )
        options_layout.addWidget(priority_label)
        options_layout.addWidget(self.priority_combo)
        
        # 重复选择
        repeat_label = QLabel(self.translator.get('repeat') + ':')
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItem(self.translator.get('never'), 'never')
        self.repeat_combo.addItem(self.translator.get('daily'), 'daily')
        self.repeat_combo.addItem(self.translator.get('weekly'), 'weekly')
        self.repeat_combo.addItem(self.translator.get('monthly'), 'monthly')
        self.repeat_combo.addItem(self.translator.get('yearly'), 'yearly')
        options_layout.addWidget(repeat_label)
        options_layout.addWidget(self.repeat_combo)
        
        # 提醒通知
        alert_label = QLabel(self.translator.get('reminder_alert') + ':')
        self.alert_combo = QComboBox()
        self.alert_combo.addItem('None', 'none')
        self.alert_combo.addItem(self.translator.get('15_min_before'), '15min')
        self.alert_combo.addItem(self.translator.get('1_hour_before'), '1hour')
        self.alert_combo.addItem(self.translator.get('1_day_before'), '1day')
        options_layout.addWidget(alert_label)
        options_layout.addWidget(self.alert_combo)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton(self.translator.get('save'))
        save_btn.clicked.connect(self.save_reminder)
        
        cancel_btn = QPushButton(self.translator.get('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def on_all_day_changed(self):
        """处理全天选项改变"""
        enabled = not self.all_day_check.isChecked()
        self.time_edit.setEnabled(enabled)
    
    def load_reminder_data(self):
        """加载提醒数据"""
        if not self.reminder_data:
            return
        
        self.title_input.setText(self.reminder_data.get('title', ''))
        self.notes_input.setText(self.reminder_data.get('description', ''))
        
        # 设置列表
        list_id = self.reminder_data.get('list_id', 'default')
        for i in range(self.list_combo.count()):
            if self.list_combo.itemData(i) == list_id:
                self.list_combo.setCurrentIndex(i)
                break
        
        # 设置日期时间
        if self.reminder_data.get('due_date'):
            date = QDate.fromString(self.reminder_data['due_date'], 'yyyy-MM-dd')
            self.date_edit.setDate(date)
        
        if self.reminder_data.get('due_time'):
            time = QTime.fromString(self.reminder_data['due_time'], 'hh:mm')
            self.time_edit.setTime(time)
        
        # 设置全天
        all_day = self.reminder_data.get('all_day', False)
        self.all_day_check.setChecked(all_day)
        self.time_edit.setEnabled(not all_day)
        
        # 设置优先级
        priority = self.reminder_data.get('priority', 0)
        for i in range(self.priority_combo.count()):
            if self.priority_combo.itemData(i) == priority:
                self.priority_combo.setCurrentIndex(i)
                break
        
        # 设置重复
        repeat = self.reminder_data.get('repeat', 'never')
        for i in range(self.repeat_combo.count()):
            if self.repeat_combo.itemData(i) == repeat:
                self.repeat_combo.setCurrentIndex(i)
                break
        
        # 设置提醒
        alert = self.reminder_data.get('alert', 'none')
        for i in range(self.alert_combo.count()):
            if self.alert_combo.itemData(i) == alert:
                self.alert_combo.setCurrentIndex(i)
                break
    
    def save_reminder(self):
        """保存提醒"""
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self, 
                'Validation', 
                self.translator.get('reminder_title') + ' is required'
            )
            return
        
        reminder_data = {
            'title': self.title_input.text(),
            'description': self.notes_input.toPlainText(),
            'list_id': self.list_combo.currentData(),
            'due_date': self.date_edit.date().toString('yyyy-MM-dd'),
            'due_time': self.time_edit.time().toString('hh:mm'),
            'all_day': self.all_day_check.isChecked(),
            'priority': self.priority_combo.currentData(),
            'repeat': self.repeat_combo.currentData(),
            'alert': self.alert_combo.currentData(),
        }
        
        self.reminder_saved.emit(reminder_data)
        self.accept()

class ListDialog(QDialog):
    """列表编辑对话框"""
    
    list_saved = pyqtSignal(dict)
    
    def __init__(self, parent=None, list_data=None):
        """初始化对话框
        
        Args:
            parent: 父窗口
            list_data: 列表数据（编辑模式）
        """
        super().__init__(parent)
        self.list_data = list_data
        self.translator = get_translator()
        self.is_edit_mode = list_data is not None
        
        self.initUI()
        self.load_list_data()
    
    def initUI(self):
        """初始化UI"""
        title = 'Edit List' if self.is_edit_mode else self.translator.get('new_list')
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        # 列表名称
        name_label = QLabel(self.translator.get('list_name') + ':')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter list name...')
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        
        # 颜色选择
        color_label = QLabel('Color:')
        self.color_combo = QComboBox()
        colors = [
            ('#007AFF', 'Blue'),
            ('#FF3B30', 'Red'),
            ('#FF9500', 'Orange'),
            ('#34C759', 'Green'),
            ('#00C7BE', 'Teal'),
            ('#A2845E', 'Brown'),
            ('#5856D6', 'Purple'),
            ('#FF2D55', 'Pink'),
        ]
        for color, name in colors:
            self.color_combo.addItem(name, color)
        layout.addWidget(color_label)
        layout.addWidget(self.color_combo)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton(self.translator.get('save'))
        save_btn.clicked.connect(self.save_list)
        
        cancel_btn = QPushButton(self.translator.get('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_list_data(self):
        """加载列表数据"""
        if not self.list_data:
            return
        
        self.name_input.setText(self.list_data.get('name', ''))
        color = self.list_data.get('color', '#007AFF')
        for i in range(self.color_combo.count()):
            if self.color_combo.itemData(i) == color:
                self.color_combo.setCurrentIndex(i)
                break
    
    def save_list(self):
        """保存列表"""
        if not self.name_input.text().strip():
            QMessageBox.warning(
                self, 
                'Validation', 
                self.translator.get('list_name') + ' is required'
            )
            return
        
        list_data = {
            'name': self.name_input.text(),
            'color': self.color_combo.currentData(),
        }
        
        self.list_saved.emit(list_data)
        self.accept()
