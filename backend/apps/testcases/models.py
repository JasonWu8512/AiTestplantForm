"""
测试用例模型模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class Project(models.Model):
    """
    项目模型
    
    存储测试项目的基本信息
    """
    name = models.CharField(_('项目名称'), max_length=100)
    description = models.TextField(_('项目描述'), blank=True, null=True)
    STATUS_CHOICES = (
        ('active', _('活跃')),
        ('archived', _('归档')),
        ('deleted', _('已删除')),
    )
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='active')
    creator = models.ForeignKey(User, verbose_name=_('创建者'), on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('项目')
        verbose_name_plural = _('项目')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TestCase(models.Model):
    """
    测试用例模型
    
    存储测试用例的详细信息，包括测试步骤和预期结果
    """
    name = models.CharField(_('用例名称'), max_length=200)
    description = models.TextField(_('用例描述'), blank=True, null=True)
    PRIORITY_CHOICES = (
        ('P0', _('最高')),
        ('P1', _('高')),
        ('P2', _('中')),
        ('P3', _('低')),
    )
    priority = models.CharField(_('优先级'), max_length=2, choices=PRIORITY_CHOICES, default='P2')
    STATUS_CHOICES = (
        ('draft', _('草稿')),
        ('active', _('活跃')),
        ('deprecated', _('废弃')),
        ('deleted', _('已删除')),
    )
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='draft')
    steps = models.TextField(_('测试步骤'))
    expected_results = models.TextField(_('预期结果'))
    project = models.ForeignKey(Project, verbose_name=_('所属项目'), on_delete=models.CASCADE, related_name='test_cases')
    creator = models.ForeignKey(User, verbose_name=_('创建者'), on_delete=models.CASCADE, related_name='created_test_cases')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('测试用例')
        verbose_name_plural = _('测试用例')
        ordering = ['-created_at']

    def __str__(self):
        return self.name 