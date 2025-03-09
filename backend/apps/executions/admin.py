"""
测试执行管理员配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import TestExecution, TestResult


@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    """
    测试执行管理员配置
    
    配置测试执行在Django管理界面中的显示和编辑方式
    """
    list_display = ('id', 'plan', 'executor', 'status', 'start_time', 'end_time', 'created_at')
    list_filter = ('status', 'executor', 'created_at')
    search_fields = ('plan__name', 'executor__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('plan', 'executor', 'status')}),
        (_('时间信息'), {'fields': ('start_time', 'end_time', 'created_at', 'updated_at')}),
    )
    date_hierarchy = 'created_at'


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """
    测试结果管理员配置
    
    配置测试结果在Django管理界面中的显示和编辑方式
    """
    list_display = ('id', 'execution', 'case', 'status', 'executor', 'execution_time', 'created_at')
    list_filter = ('status', 'executor', 'execution_time')
    search_fields = ('case__name', 'executor__username', 'actual_result')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('execution', 'case', 'status', 'executor')}),
        (_('结果信息'), {'fields': ('actual_result', 'remarks')}),
        (_('时间信息'), {'fields': ('execution_time', 'created_at', 'updated_at')}),
    )
    date_hierarchy = 'execution_time' 