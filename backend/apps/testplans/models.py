"""
测试计划模型模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.testcases.models import TestCase, Project


class TestPlan(models.Model):
    """
    测试计划模型
    
    存储测试计划的基本信息，包括计划名称、描述、状态和时间范围
    """
    name = models.CharField(_('计划名称'), max_length=200)
    description = models.TextField(_('计划描述'), blank=True, null=True)
    STATUS_CHOICES = (
        ('draft', _('草稿')),
        ('ready', _('就绪')),
        ('in_progress', _('进行中')),
        ('completed', _('已完成')),
        ('archived', _('已归档')),
    )
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='draft')
    start_time = models.DateTimeField(_('开始时间'), blank=True, null=True)
    end_time = models.DateTimeField(_('结束时间'), blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name=_('所属项目'), on_delete=models.CASCADE, related_name='test_plans')
    creator = models.ForeignKey(User, verbose_name=_('创建者'), on_delete=models.CASCADE, related_name='created_test_plans')
    test_cases = models.ManyToManyField(TestCase, through='TestPlanCase', verbose_name=_('测试用例'), related_name='test_plans')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('测试计划')
        verbose_name_plural = _('测试计划')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TestPlanCase(models.Model):
    """
    测试计划-用例关联模型
    
    存储测试计划和测试用例的关联关系，包括执行顺序
    """
    plan = models.ForeignKey(TestPlan, verbose_name=_('测试计划'), on_delete=models.CASCADE)
    case = models.ForeignKey(TestCase, verbose_name=_('测试用例'), on_delete=models.CASCADE)
    order = models.IntegerField(_('执行顺序'), default=0)
    
    class Meta:
        verbose_name = _('测试计划-用例关联')
        verbose_name_plural = _('测试计划-用例关联')
        ordering = ['order']
        unique_together = ('plan', 'case')

    def __str__(self):
        return f"{self.plan.name} - {self.case.name}" 