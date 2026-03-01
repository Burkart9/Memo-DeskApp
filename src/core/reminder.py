"""提醒事项数据模型和存储"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
import uuid

class Priority(Enum):
    """优先级枚举"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Repeat(Enum):
    """重复枚举"""
    NEVER = 'never'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

@dataclass
class Reminder:
    """提醒事项数据模型"""
    id: str
    title: str
    description: str = ''
    list_id: str = 'default'
    due_date: Optional[str] = None  # YYYY-MM-DD
    due_time: Optional[str] = None  # HH:MM
    all_day: bool = False
    priority: int = 0
    repeat: str = 'never'
    alert: str = 'none'  # none, 15min, 1hour, 1day
    is_completed: bool = False
    is_flagged: bool = False
    created_at: str = ''
    updated_at: str = ''
    
    def __post_init__(self):
        """初始化时间戳"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建"""
        return cls(**data)

@dataclass
class ReminderList:
    """提醒列表数据模型"""
    id: str
    name: str
    color: str = '#007AFF'  # 默认蓝色
    is_smart_list: bool = False  # 是否为智能列表
    created_at: str = ''
    
    def __post_init__(self):
        """初始化时间戳"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建"""
        return cls(**data)

class ReminderStorage:
    """提醒事项存储管理"""
    
    def __init__(self, data_dir='./data'):
        """初始化存储
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.reminders_file = os.path.join(data_dir, 'reminders.json')
        self.lists_file = os.path.join(data_dir, 'lists.json')
        
        # 创建数据目录
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化数据
        self._reminders: List[Reminder] = []
        self._lists: List[ReminderList] = []
        
        # 加载数据
        self._load()
        
        # 确保有默认列表
        self._ensure_default_list()
    
    def _load(self):
        """从文件加载数据"""
        # 加载提醒事项
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._reminders = [Reminder.from_dict(item) for item in data]
            except:
                self._reminders = []
        
        # 加载列表
        if os.path.exists(self.lists_file):
            try:
                with open(self.lists_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._lists = [ReminderList.from_dict(item) for item in data]
            except:
                self._lists = []
    
    def _save(self):
        """保存数据到文件"""
        # 保存提醒事项
        with open(self.reminders_file, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self._reminders], f, 
                     ensure_ascii=False, indent=2)
        
        # 保存列表
        with open(self.lists_file, 'w', encoding='utf-8') as f:
            json.dump([l.to_dict() for l in self._lists], f, 
                     ensure_ascii=False, indent=2)
    
    def _ensure_default_list(self):
        """确保有默认列表"""
        if not any(l.id == 'default' for l in self._lists):
            default_list = ReminderList(
                id='default',
                name='Reminders',
                color='#007AFF',
                is_smart_list=False
            )
            self._lists.append(default_list)
            self._save()
    
    # 提醒事项管理
    def add_reminder(self, title: str, list_id: str = 'default', 
                    description: str = '', due_date: Optional[str] = None,
                    due_time: Optional[str] = None, all_day: bool = False,
                    priority: int = 0, repeat: str = 'never',
                    alert: str = 'none') -> Reminder:
        """添加新提醒"""
        reminder = Reminder(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            list_id=list_id,
            due_date=due_date,
            due_time=due_time,
            all_day=all_day,
            priority=priority,
            repeat=repeat,
            alert=alert
        )
        self._reminders.append(reminder)
        self._save()
        return reminder
    
    def update_reminder(self, reminder_id: str, **kwargs):
        """更新提醒"""
        for reminder in self._reminders:
            if reminder.id == reminder_id:
                for key, value in kwargs.items():
                    if hasattr(reminder, key):
                        setattr(reminder, key, value)
                reminder.updated_at = datetime.now().isoformat()
                self._save()
                return reminder
        return None
    
    def delete_reminder(self, reminder_id: str):
        """删除提醒"""
        self._reminders = [r for r in self._reminders if r.id != reminder_id]
        self._save()
    
    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """获取单个提醒"""
        for reminder in self._reminders:
            if reminder.id == reminder_id:
                return reminder
        return None
    
    def get_all_reminders(self) -> List[Reminder]:
        """获取所有提醒"""
        return self._reminders.copy()
    
    def get_reminders_by_list(self, list_id: str) -> List[Reminder]:
        """获取指定列表的提醒"""
        return [r for r in self._reminders if r.list_id == list_id]
    
    def get_today_reminders(self) -> List[Reminder]:
        """获取今天的提醒"""
        today = datetime.now().strftime('%Y-%m-%d')
        return [r for r in self._reminders 
                if r.due_date == today and not r.is_completed]
    
    def get_flagged_reminders(self) -> List[Reminder]:
        """获取标记的提醒"""
        return [r for r in self._reminders if r.is_flagged and not r.is_completed]
    
    def get_completed_reminders(self) -> List[Reminder]:
        """获取完成的提醒"""
        return [r for r in self._reminders if r.is_completed]
    
    def get_pending_reminders(self) -> List[Reminder]:
        """获取未完成的提醒"""
        return [r for r in self._reminders if not r.is_completed]
    
    # 列表管理
    def add_list(self, name: str, color: str = '#007AFF') -> ReminderList:
        """添加新列表"""
        reminder_list = ReminderList(
            id=str(uuid.uuid4()),
            name=name,
            color=color,
            is_smart_list=False
        )
        self._lists.append(reminder_list)
        self._save()
        return reminder_list
    
    def update_list(self, list_id: str, **kwargs):
        """更新列表"""
        for reminder_list in self._lists:
            if reminder_list.id == list_id:
                for key, value in kwargs.items():
                    if hasattr(reminder_list, key):
                        setattr(reminder_list, key, value)
                self._save()
                return reminder_list
        return None
    
    def delete_list(self, list_id: str):
        """删除列表及其中的提醒"""
        self._lists = [l for l in self._lists if l.id != list_id]
        self._reminders = [r for r in self._reminders if r.list_id != list_id]
        self._save()
    
    def get_all_lists(self) -> List[ReminderList]:
        """获取所有列表"""
        return self._lists.copy()
    
    def get_list(self, list_id: str) -> Optional[ReminderList]:
        """获取单个列表"""
        for reminder_list in self._lists:
            if reminder_list.id == list_id:
                return reminder_list
        return None
    
    def get_smart_lists(self) -> List[ReminderList]:
        """获取智能列表"""
        return [l for l in self._lists if l.is_smart_list]
    
    def get_custom_lists(self) -> List[ReminderList]:
        """获取自定义列表"""
        return [l for l in self._lists if not l.is_smart_list]

# 全局存储实例
_storage = None

def get_storage(data_dir='./data') -> ReminderStorage:
    """获取存储实例"""
    global _storage
    if _storage is None:
        _storage = ReminderStorage(data_dir)
    return _storage
