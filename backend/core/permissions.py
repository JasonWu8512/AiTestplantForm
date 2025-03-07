"""
权限模块，提供自定义权限类

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    仅允许管理员用户访问
    """
    
    def has_permission(self, request, view):
        """
        检查用户是否有权限执行操作
        
        Args:
            request: HTTP请求对象
            view: 视图对象
            
        Returns:
            bool: 如果用户是管理员则返回True，否则返回False
        """
        return bool(request.user and request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限，仅允许对象的创建者编辑它
    """
    
    def has_object_permission(self, request, view, obj):
        """
        检查用户是否有权限操作特定对象
        
        Args:
            request: HTTP请求对象
            view: 视图对象
            obj: 要操作的对象
            
        Returns:
            bool: 如果是安全方法或用户是对象创建者则返回True
        """
        # 读取权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # 写入权限仅允许对象的创建者
        return obj.creator == request.user 