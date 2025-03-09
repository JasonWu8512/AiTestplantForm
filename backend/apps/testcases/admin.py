"""
测试用例管理员配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Project, TestCase


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    项目管理员配置
    
    配置项目在Django管理界面中的显示和编辑方式
    """
    list_display = ('id', 'name', 'status', 'creator', 'created_at', 'updated_at')
    list_filter = ('status', 'creator', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'status', 'creator')}),
        (_('时间信息'), {'fields': ('created_at', 'updated_at')}),
    )
    date_hierarchy = 'created_at'


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    """
    测试用例管理员配置
    
    配置测试用例在Django管理界面中的显示和编辑方式
    """
    list_display = ('id', 'name', 'project', 'priority', 'status', 'creator', 'created_at')
    list_filter = ('project', 'priority', 'status', 'creator', 'created_at')
    search_fields = ('name', 'description', 'steps', 'expected_results')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'project', 'creator')}),
        (_('用例信息'), {'fields': ('priority', 'status', 'steps', 'expected_results')}),
        (_('时间信息'), {'fields': ('created_at', 'updated_at')}),
    )
    date_hierarchy = 'created_at' 