"""
权限模块，定义自定义权限类

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import permissions
from .constants import USER_ROLE_ADMIN

class IsAdmin(permissions.BasePermission):
    """
    只允许管理员访问
    """
    message = "只有管理员可以执行此操作。"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == USER_ROLE_ADMIN

class IsOwner(permissions.BasePermission):
    """
    只允许对象的所有者访问
    """
    message = "您不是此资源的所有者。"

    def has_object_permission(self, request, view, obj):
        # 假设对象有一个user属性表示所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # 如果对象有一个created_by属性表示创建者
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        # 如果对象是用户本身
        elif hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        return False

class IsProjectMember(permissions.BasePermission):
    """
    只允许项目成员访问
    """
    message = "您不是此项目的成员。"

    def has_object_permission(self, request, view, obj):
        # 获取项目对象
        project = None
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'test_plan') and hasattr(obj.test_plan, 'project'):
            project = obj.test_plan.project
        elif hasattr(obj, 'test_case') and hasattr(obj.test_case, 'project'):
            project = obj.test_case.project
        
        if not project:
            return False
            
        # 检查用户是否是项目成员
        return project.members.filter(id=request.user.id).exists()

class ReadOnly(permissions.BasePermission):
    """
    只允许只读操作
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    管理员可以执行所有操作，其他用户只能读取
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == USER_ROLE_ADMIN

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    所有者可以执行所有操作，其他用户只能读取
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # 假设对象有一个user属性表示所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # 如果对象有一个created_by属性表示创建者
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        # 如果对象是用户本身
        elif hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        return False 