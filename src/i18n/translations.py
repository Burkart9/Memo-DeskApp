"""多语言文本管理模块"""

TRANSLATIONS = {
    'en': {
        # 主窗口标题和菜单
        'app_title': 'Reminders',
        'today': 'Today',
        'scheduled': 'Scheduled',
        'all': 'All',
        'flagged': 'Flagged',
        
        # 操作按钮
        'add_reminder': 'Add Reminder',
        'new_list': 'New List',
        'delete': 'Delete',
        'edit': 'Edit',
        'mark_complete': 'Mark Complete',
        'add_priority': 'Set Priority',
        
        # 优先级
        'priority': 'Priority',
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low',
        'no_priority': 'None',
        
        # 日期和时间
        'due_date': 'Due Date',
        'due_time': 'Due Time',
        'all_day': 'All-day',
        'repeat': 'Repeat',
        'never': 'Never',
        'daily': 'Every day',
        'weekly': 'Every week',
        'monthly': 'Every month',
        'yearly': 'Every year',
        
        # 提示和通知
        'add_notes': 'Add Notes',
        'notes': 'Notes',
        'reminder_alert': 'Reminder Alert',
        '15_min_before': '15 minutes before',
        '1_hour_before': '1 hour before',
        '1_day_before': '1 day before',
        
        # 对话框标题
        'add_new_reminder': 'Add New Reminder',
        'edit_reminder': 'Edit Reminder',
        'new_list': 'New List',
        'list_name': 'List Name',
        'reminder_title': 'Reminder Title',
        
        # 菜单
        'file': 'File',
        'edit': 'Edit',
        'view': 'View',
        'help': 'Help',
        'exit': 'Exit',
        'settings': 'Settings',
        'about': 'About',
        'dark_mode': 'Dark Mode',
        'language': 'Language',
        
        # 空状态提示
        'no_reminders': 'No reminders',
        'add_first_reminder': 'Add your first reminder to get started',
        
        # 确认对话框
        'confirm_delete': 'Are you sure you want to delete this reminder?',
        'confirm_delete_list': 'Are you sure you want to delete this list?',
        'yes': 'Yes',
        'no': 'No',
        'cancel': 'Cancel',
        'ok': 'OK',
        'save': 'Save',
        
        # 状态提示
        'saved': 'Saved',
        'deleted': 'Deleted',
        'created': 'Created',
    },
    'zh': {
        # 主窗口标题和菜单
        'app_title': '提醒事项',
        'today': '今天',
        'scheduled': '计划',
        'all': '全部',
        'flagged': '标记',
        
        # 操作按钮
        'add_reminder': '添加提醒',
        'new_list': '新列表',
        'delete': '删除',
        'edit': '编辑',
        'mark_complete': '标记完成',
        'add_priority': '设置优先级',
        
        # 优先级
        'priority': '优先级',
        'high': '高',
        'medium': '中',
        'low': '低',
        'no_priority': '无',
        
        # 日期和时间
        'due_date': '完成日期',
        'due_time': '完成时间',
        'all_day': '全天',
        'repeat': '重复',
        'never': '从不',
        'daily': '每天',
        'weekly': '每周',
        'monthly': '每月',
        'yearly': '每年',
        
        # 提示和通知
        'add_notes': '添加备注',
        'notes': '备注',
        'reminder_alert': '提醒通知',
        '15_min_before': '提前15分钟',
        '1_hour_before': '提前1小时',
        '1_day_before': '提前1天',
        
        # 对话框标题
        'add_new_reminder': '添加新提醒',
        'edit_reminder': '编辑提醒',
        'new_list': '新列表',
        'list_name': '列表名称',
        'reminder_title': '提醒标题',
        
        # 菜单
        'file': '文件',
        'edit': '编辑',
        'view': '视图',
        'help': '帮助',
        'exit': '退出',
        'settings': '设置',
        'about': '关于',
        'dark_mode': '深色模式',
        'language': '语言',
        
        # 空状态提示
        'no_reminders': '没有提醒',
        'add_first_reminder': '添加你的第一个提醒开始使用',
        
        # 确认对话框
        'confirm_delete': '确定要删除此提醒吗？',
        'confirm_delete_list': '确定要删除此列表吗？',
        'yes': '是',
        'no': '否',
        'cancel': '取消',
        'ok': '确定',
        'save': '保存',
        
        # 状态提示
        'saved': '已保存',
        'deleted': '已删除',
        'created': '已创建',
    }
}

class Translator:
    """翻译器类"""
    
    def __init__(self, language='en'):
        """初始化翻译器
        
        Args:
            language: 语言代码 ('en' 或 'zh')
        """
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    
    def set_language(self, language):
        """设置语言"""
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    
    def get(self, key, default=''):
        """获取翻译文本"""
        return self.translations.get(key, default)
    
    def _(self, key):
        """简写获取翻译"""
        return self.get(key)


# 全局翻译器实例
_translator = Translator('en')

def set_language(language):
    """设置全局语言"""
    _translator.set_language(language)

def _(key):
    """全局翻译函数"""
    return _translator.get(key)

def get_translator():
    """获取翻译器实例"""
    return _translator
