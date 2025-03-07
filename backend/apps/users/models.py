"""
用户模型模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    自定义用户模型
    
    扩展Django的AbstractUser，添加额外的用户信息字段
    """
    phone = models.CharField(_('手机号'), max_length=20, blank=True, null=True)
    department = models.CharField(_('部门'), max_length=100, blank=True, null=True)
    position = models.CharField(_('职位'), max_length=100, blank=True, null=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(_('激活状态'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username 