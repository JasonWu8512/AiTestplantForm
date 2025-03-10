"""
测试报告模型模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.executions.models import TestExecution


class Report(models.Model):
    """
    测试报告模型
    
    存储测试报告的基本信息
    """
    name = models.CharField(_('报告名称'), max_length=200)
    description = models.TextField(_('报告描述'), blank=True, null=True)
    execution = models.ForeignKey(TestExecution, verbose_name=_('关联执行'), on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(_('报告类型'), max_length=50, choices=[
        ('allure', 'Allure报告'),
        ('html', 'HTML报告'),
        ('pdf', 'PDF报告'),
    ], default='allure')
    file_path = models.CharField(_('文件路径'), max_length=500)
    is_public = models.BooleanField(_('是否公开'), default=True)
    creator = models.ForeignKey(User, verbose_name=_('创建者'), on_delete=models.CASCADE, related_name='created_reports')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('测试报告')
        verbose_name_plural = _('测试报告')
        ordering = ['-created_at']

    def __str__(self):
        return self.name 