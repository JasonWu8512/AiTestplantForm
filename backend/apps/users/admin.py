"""
用户管理员配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    用户管理员配置
    
    扩展Django默认的用户管理员配置，添加自定义字段
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'department', 'position', 'avatar')}),
        (_('权限'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('重要日期'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'department')
    ordering = ('username',) 