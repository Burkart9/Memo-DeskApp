"""应用配置管理"""

import json
import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    """应用配置管理器"""
    
    def __init__(self, config_dir: str = None):
        """初始化配置管理器
        
        Args:
            config_dir: 配置目录路径
        """
        if config_dir is None:
            config_dir = str(Path.home() / '.reminders-app')
        
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, 'config.json')
        
        # 创建配置目录
        os.makedirs(config_dir, exist_ok=True)
        
        # 默认配置
        self.defaults = {
            'theme': 'light',
            'language': 'en',
            'window_width': 1000,
            'window_height': 600,
            'window_x': 100,
            'window_y': 100,
        }
        
        self.config = self.defaults.copy()
        self._load()
    
    def _load(self):
        """从文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # 合并加载的配置和默认值
                    self.config = {**self.defaults, **loaded}
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = self.defaults.copy()
    
    def _save(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
        self._save()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self.config.copy()

# 全局配置实例
_config = None

def get_config(config_dir: str = None) -> AppConfig:
    """获取全局配置实例"""
    global _config
    if _config is None:
        _config = AppConfig(config_dir)
    return _config
