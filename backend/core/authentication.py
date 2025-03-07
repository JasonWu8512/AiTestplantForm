"""
认证模块，提供JWT认证相关功能

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义JWT认证类
    
    扩展了标准的JWT认证，可以添加自定义的认证逻辑
    """
    
    def authenticate(self, request):
        """
        执行认证过程
        
        Args:
            request: HTTP请求对象
            
        Returns:
            tuple: (user, token)元组，如果认证失败则返回None
        """
        # 调用父类的认证方法
        result = super().authenticate(request)
        
        if result is not None:
            # 认证成功，可以在这里添加自定义逻辑
            user, token = result
            # 例如，检查用户状态
            if not user.is_active:
                return None
        
        return result 