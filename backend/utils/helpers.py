"""
辅助函数模块，提供各种实用工具函数

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import uuid
import json
import datetime
from django.utils import timezone

def generate_unique_id():
    """
    生成唯一ID
    
    Returns:
        str: UUID字符串
    """
    return str(uuid.uuid4())

def get_current_time():
    """
    获取当前时间（带时区）
    
    Returns:
        datetime: 当前时间
    """
    return timezone.now()

def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """
    格式化日期时间
    
    Args:
        dt (datetime): 日期时间对象
        format_str (str): 格式字符串
        
    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        return None
    return dt.strftime(format_str)

def parse_datetime(dt_str, format_str="%Y-%m-%d %H:%M:%S"):
    """
    解析日期时间字符串
    
    Args:
        dt_str (str): 日期时间字符串
        format_str (str): 格式字符串
        
    Returns:
        datetime: 解析后的日期时间对象
    """
    if not dt_str:
        return None
    return datetime.datetime.strptime(dt_str, format_str)

def json_dumps(data):
    """
    将数据转换为JSON字符串
    
    Args:
        data: 要转换的数据
        
    Returns:
        str: JSON字符串
    """
    return json.dumps(data, ensure_ascii=False)

def json_loads(json_str):
    """
    将JSON字符串转换为Python对象
    
    Args:
        json_str (str): JSON字符串
        
    Returns:
        object: Python对象
    """
    if not json_str:
        return None
    return json.loads(json_str)

def truncate_string(s, max_length=100, suffix='...'):
    """
    截断字符串
    
    Args:
        s (str): 原始字符串
        max_length (int): 最大长度
        suffix (str): 后缀
        
    Returns:
        str: 截断后的字符串
    """
    if not s:
        return ''
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix 