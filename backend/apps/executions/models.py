"""
测试执行模型模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.testplans.models import TestPlan
from apps.testcases.models import TestCase


class TestExecution(models.Model):
    """
    测试执行模型
    
    存储测试执行的基本信息，包括执行状态、开始和结束时间
    """
    plan = models.ForeignKey(TestPlan, verbose_name=_('测试计划'), on_delete=models.CASCADE, related_name='executions')
    executor = models.ForeignKey(User, verbose_name=_('执行者'), on_delete=models.CASCADE, related_name='executed_tests')
    STATUS_CHOICES = (
        ('pending', _('待执行')),
        ('running', _('执行中')),
        ('paused', _('已暂停')),
        ('completed', _('已完成')),
        ('aborted', _('已中止')),
    )
    status = models.CharField(_('执行状态'), max_length=20, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(_('开始时间'), blank=True, null=True)
    end_time = models.DateTimeField(_('结束时间'), blank=True, null=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('测试执行')
        verbose_name_plural = _('测试执行')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.plan.name} - {self.get_status_display()}"


class TestResult(models.Model):
    """
    测试结果模型
    
    存储测试用例的执行结果，包括状态、实际结果和备注
    """
    execution = models.ForeignKey(TestExecution, verbose_name=_('测试执行'), on_delete=models.CASCADE, related_name='results')
    case = models.ForeignKey(TestCase, verbose_name=_('测试用例'), on_delete=models.CASCADE, related_name='results')
    STATUS_CHOICES = (
        ('pending', _('待执行')),
        ('passed', _('通过')),
        ('failed', _('失败')),
        ('blocked', _('阻塞')),
        ('skipped', _('跳过')),
    )
    status = models.CharField(_('结果状态'), max_length=20, choices=STATUS_CHOICES, default='pending')
    actual_result = models.TextField(_('实际结果'), blank=True, null=True)
    remarks = models.TextField(_('备注'), blank=True, null=True)
    executor = models.ForeignKey(User, verbose_name=_('执行者'), on_delete=models.CASCADE, related_name='test_results', blank=True, null=True)
    execution_time = models.DateTimeField(_('执行时间'), blank=True, null=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('测试结果')
        verbose_name_plural = _('测试结果')
        ordering = ['-updated_at']
        unique_together = ('execution', 'case')

    def __str__(self):
        return f"{self.case.name} - {self.get_status_display()}" 