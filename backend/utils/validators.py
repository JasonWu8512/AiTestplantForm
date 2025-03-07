"""
验证器模块，提供各种数据验证函数

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_username(username):
    """
    验证用户名
    
    Args:
        username (str): 用户名
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValidationError(
            _('用户名必须是3-20个字符，只能包含字母、数字和下划线')
        )

def validate_password(password):
    """
    验证密码强度
    
    Args:
        password (str): 密码
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if len(password) < 8:
        raise ValidationError(_('密码长度必须至少为8个字符'))
    
    if not any(char.isdigit() for char in password):
        raise ValidationError(_('密码必须包含至少一个数字'))
    
    if not any(char.isalpha() for char in password):
        raise ValidationError(_('密码必须包含至少一个字母'))

def validate_phone(phone):
    """
    验证手机号
    
    Args:
        phone (str): 手机号
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if not re.match(r'^1[3-9]\d{9}$', phone):
        raise ValidationError(_('请输入有效的手机号码'))

def validate_email(email):
    """
    验证邮箱
    
    Args:
        email (str): 邮箱
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValidationError(_('请输入有效的邮箱地址'))

def validate_url(url):
    """
    验证URL
    
    Args:
        url (str): URL
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if not re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
        raise ValidationError(_('请输入有效的URL地址'))

def validate_positive_number(value):
    """
    验证正数
    
    Args:
        value (int/float): 数值
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if value <= 0:
        raise ValidationError(_('值必须大于0'))

def validate_file_extension(value, allowed_extensions=None):
    """
    验证文件扩展名
    
    Args:
        value: 文件对象
        allowed_extensions (list): 允许的扩展名列表
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        
    import os
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            _('不支持的文件类型。允许的类型: %(extensions)s'),
            params={'extensions': ', '.join(allowed_extensions)},
        )

def validate_file_size(value, max_size=5*1024*1024):  # 默认5MB
    """
    验证文件大小
    
    Args:
        value: 文件对象
        max_size (int): 最大文件大小（字节）
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    if value.size > max_size:
        raise ValidationError(
            _('文件太大。最大允许大小为 %(max_size)s MB'),
            params={'max_size': max_size/1024/1024},
        ) 