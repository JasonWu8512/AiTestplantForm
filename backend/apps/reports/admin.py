"""
测试报告管理员配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    测试报告管理员配置
    
    配置测试报告在Django管理后台的显示和编辑方式
    """
    list_display = ('id', 'name', 'execution', 'report_type', 'is_public', 'creator', 'created_at')
    list_filter = ('report_type', 'is_public', 'created_at')
    search_fields = ('name', 'description', 'execution__plan__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'execution', 'report_type', 'is_public')
        }),
        ('文件信息', {
            'fields': ('file_path',)
        }),
        ('创建信息', {
            'fields': ('creator', 'created_at', 'updated_at')
        }),
    ) 